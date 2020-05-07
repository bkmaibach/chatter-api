# chatter/routing.py
from django.urls import re_path
from . import consumers

# WEBSOCKETS - The routing is kind of like the urls.py but for a different protocol
# This routing.py is in turn registered in the project routing.py
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_id>\w+)', consumers.ChatConsumer)
]