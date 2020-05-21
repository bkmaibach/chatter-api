# chat/consumers.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.hashers import check_password
from channels.db import database_sync_to_async

from .models import Entry
from .models import Room
from asgiref.sync import sync_to_async
from .serializers import MessageSerializer
from .serializers import EntrySerializer

@database_sync_to_async
def get_user(token_key):
    try:
        token = Token.objects.get(key=token_key)
        return token.user
    except Token.DoesNotExist:
        return AnonymousUser()

@database_sync_to_async
def create_entry(author, text, room_id):
    return Entry.objects.create(author=author, text=text, room_id=int(room_id))

# @database_sync_to_async
# def get_latest_messages(room_id):
#     return sync_to_async(Entry.last_50_messages, thread_sensitive=True)(room_id=room_id)

@database_sync_to_async
def check_room_password(room_id, password):
    hashed_password = Room.objects.get(id=room_id).password
    print('GOT HASHED PASSWORD ', hashed_password)
    print('CHECKING PASSWORD ', password)
    if not hashed_password:
        return True
    else:
        return check_password(password, hashed_password)

# WEBSOCKETS - The consumer is like the view for websockets.
# It is registered in the app routing.py
class ChatConsumer(AsyncWebsocketConsumer):
    INIT_CHAT = 'INIT_CHAT'
    FETCH_ENTRIES = 'FETCH_ENTRIES'
    NEW_ENTRY = 'NEW_ENTRY'
    ENTRIES = 'ENTRIES'
    ERROR = 'ERROR'
    INIT_RESPONSE = 'INIT_RESPONSE'
    
    async def connect(self):
        print('CONNECTION RECEIVED')
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat_{0}'.format(self.room_id)
        # print("ROOM GROUP NAME " + self.room_group_name)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def init_chat(self, isAuthorized):
        # user = await get_user(data['token'])
        message = {
            'command': self.INIT_RESPONSE,
            'authorized': isAuthorized
        }
        print('INIT_CHAT RECEIVED, RESPONDING WITH ', message)
        await self.send_message(message)

    async def fetch_entries(self, data):
        messages = Entry.last_50_entries(room_id=self.room_id)
        message = {
            'command': self.ENTRIES,
            'entries': self.entries_to_json(messages)
        }
        # print('SENDING CONTENT', content)
        await self.send_message(message)

    async def new_entry(self, data):
        # print('NEW_MESSAGE command received')
        # print(data)
        text = data['text']
        user = await get_user(data['token'])
        # print("GOT USER: " + str(user))
        # print("SELF SCOPE IS: " + str(self.scope))
        entry = await create_entry(user, text, self.room_id)
        
        content = {
            'command': self.NEW_ENTRY,
            'entry': self.entry_to_json(entry)
        }
        await self.send_chat_message(content)

    async def error_reponse(self, error):
        content = {
            'command': self.ERROR,
            'error': error
        }
        await self.send_message(content)

    async def receive(self, text_data):
        print('IN RECEIVE WITH MESSAGE STRING ' + text_data)
        message = json.loads(text_data)
        message_serializer = MessageSerializer(data=message)

        if message_serializer.is_valid():
            print('VALID SERIALIZER: ', message_serializer.validated_data)
            validMessage = message_serializer.validated_data
            password = validMessage['password']
            isAuthorized = await check_room_password(self.room_id, password)
            if validMessage['command'] == ChatConsumer.INIT_CHAT:
                await self.init_chat(isAuthorized)
            elif isAuthorized:
                if validMessage['command'] == ChatConsumer.FETCH_ENTRIES:
                    await self.fetch_entries(validMessage)
                elif validMessage['command'] == ChatConsumer.NEW_ENTRY:
                    await self.new_entry(validMessage)
                else:
                    await self.error_reponse('No procedure is available for command \"{0}\"'
                        .format(validMessage['command']))
            else:
                await self.error_reponse('The password was incorrect')
        else:
            await self.error_reponse('The data sent could not be recognized')
            print('INVALID SERIALIZER: ', message_serializer.errors)
        

    async def send_message(self, message):
        # print('Sending message: ' + json.dumps(message))
        await self.send(text_data=json.dumps(message))

    async def send_chat_message(self, message):
        # Send message to room group
        # print('GROUP SENDING MESSAGE ' + str(message))
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        # print('IN CHAT MESSAGE WITH ' + json.dumps(message))
        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))

    def entry_to_json(self, entry):
        entryJson = {
            'id': str(entry.id),
            'author': str(entry.author),
            'text': entry.text,
            'timestamp': str(entry.timestamp)
        }
        return entryJson

    def entries_to_json(self, entries):
        result = []
        for entry in entries:
            result.append(self.entry_to_json(entry))
        return result
