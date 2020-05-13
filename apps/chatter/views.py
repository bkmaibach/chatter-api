from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from .models import Room
from .serializers import RoomSerializer
from rest_framework.authentication import TokenAuthentication

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

# class RoomMessageViewSet(viewsets.ModelViewSet):
#     """Handles creating reading and updating Messages"""
#     authentication_classes = (TokenAuthentication,)
#     serializer_class = serializers.MessageSerializer
#     queryset = models.Messages.objects.all()
#     permission_classes = (permissions.SendOwnMessages, IsAuthenticated)

#     def perform_create(self, serializer):
#         """Sets the UserProfile to the logged in user"""
#         serializer.save(user_profile=self.request.user)