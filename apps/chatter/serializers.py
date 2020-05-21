from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from django.contrib.auth import hashers

from .models import Room, Entry
# from .constants import INIT_CHAT, FETCH_ENTRIES, NEW_ENTRY, ENTRIES, ERROR, INIT_RESPONSE

class RoomSerializer(serializers.HyperlinkedModelSerializer):
    has_password = serializers.SerializerMethodField()
    class Meta:
        model = Room
        fields = ['id', 'name', 'password', 'has_password']
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True}
        }

    def create(self, validated_data):
        if 'password' in validated_data:
            password_hash = hashers.make_password(validated_data['password'])
            validated_data['password'] = password_hash
        else:
            validated_data['password'] = ''
        return Room.objects.create(**validated_data)

    def get_has_password(self, obj):
        return obj.password is not ''

class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ('timestamp', 'author', 'text')
        extra_kwargs = {
            'author': {'read_only': True},
            'timestamp': {'read_only': True}
        }

class MessageSerializer(serializers.Serializer):
    command = serializers.CharField(max_length=32)
    token = serializers.CharField(required=False, min_length=40, max_length=40)
    text = serializers.CharField(required=False, max_length=255)
    password = serializers.CharField(max_length=255, allow_blank=True)
    # Not necessary at this end of the API?
    # entries = EntrySerializer(required=False, many=True)
    success = serializers.CharField(required=False, max_length=100)
    error = serializers.CharField(required=False, max_length=100)

    # def create(self, validated_data):
    #     if validated_data['tracks'] is 'NEW_ENTRY':
    #         entry = Entry.objects.create(**validated_data['entry'])

