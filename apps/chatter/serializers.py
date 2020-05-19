from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from .models import Room, Entry

class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name']

class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ('id', 'timestamp', 'author', 'text')
        extra_kwargs = {'author': {'read_only': True}}

class MessageSerializer(serializers.Serializer):
    command = serializers.ChoiceField(choices=['INIT_CHAT', 'FETCH_ENTRIES', 'NEW_ENTRY', 'ENTRIES'])
    token = serializers.CharField(required=False, min_length=40, max_length=40)
    text = serializers.CharField(required=False, max_length=255)
    # Not necessary at this end of the API?
    # entries = EntrySerializer(required=False, many=True)
    success = serializers.CharField(required=False, max_length=100)
    error = serializers.CharField(required=False, max_length=100)

    # def create(self, validated_data):
    #     if validated_data['tracks'] is 'NEW_ENTRY':
    #         entry = Entry.objects.create(**validated_data['entry'])

