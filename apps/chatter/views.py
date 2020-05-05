from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from .models import Room
from .serializers import RoomSerializer

class RoomViewSet(viewsets.ModelViewSet):
    """API endpoint that allows rooms to be viewed or edited."""
    queryset = Room.objects.all().order_by('name')
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]

def index(request):
    return render(request, 'chatter/index.html')

def room(request, room_name):
    return render(request, 'chatter/room.html', {
        'room_name': room_name
    })