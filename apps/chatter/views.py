from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication

from .models import Room
from .serializers import RoomSerializer

class RoomViewSet(viewsets.ModelViewSet):
    """API endpoint that allows rooms to be viewed or edited."""
    queryset = Room.objects.all().order_by('name')
    serializer_class = RoomSerializer
    permission_classes = (permissions.IsAuthenticated,)
