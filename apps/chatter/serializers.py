from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from .models import Room, Entry

class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name']

class EntrySerializer(serializers.Serializer):
    class Meta:
        model = Entry
        fields = ('id', 'timestamp', 'author', 'text')
        extra_kwargs = {'author': {'read_only': True}}