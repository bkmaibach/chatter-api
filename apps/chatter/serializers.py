from rest_framework import serializers
from .models import Room, Message

class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name']

class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'timestamp', 'author', 'text')
        extra_kwargs = {'author': {'read_only': True}}