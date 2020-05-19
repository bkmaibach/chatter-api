from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from .models import Room
from .serializers import RoomSerializer
from rest_framework.authentication import TokenAuthentication

class RoomViewSet(viewsets.ModelViewSet):
    """API endpoint that allows rooms to be viewed or edited."""
    authentication_classes = (TokenAuthentication,)
    queryset = Room.objects.all().order_by('name')
    serializer_class = RoomSerializer
    permission_classes = (permissions.IsAuthenticated,)