from rest_framework import serializers
from .models import Room, Message

class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        fields = ['name', 'id']

class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'timestamp', 'user_profile', 'text')
        extra_kwargs = {'user_profile': {'read_only': True}}