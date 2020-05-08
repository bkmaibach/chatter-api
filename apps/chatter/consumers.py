# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework.authtoken.models import Token
from channels.db import database_sync_to_async
# from .models import Message
# from .models import Room

@database_sync_to_async
def get_user(token_key):
    try:
        token = Token.objects.get(key=token_key)
        return token.user
    except Token.DoesNotExist:
        return AnonymousUser()

# WEBSOCKETS - The consumer is like the view for websockets.
# It is registered in the app routing.py
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('CONNECTION RECEIVED')
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat_{0}'.format(self.room_id)
        print("ROOM GROUP NAME " + self.room_group_name)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self):
        print('CONNECTION LOST')
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print('MESSAGE RECEIVED')

        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        command = text_data_json['command']
        token = text_data_json['token']
        user = await get_user(token)
        print("GOT USER: " + str(user))
        print("SELF SCOPE IS: " + str(self.scope))
        # print('Authenticated user id: ' + str(self.scope['user']))

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        print('CHAT MESSAGE CALLED')
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
