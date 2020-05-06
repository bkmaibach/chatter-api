from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import apps.chatter.routing

# WEBSOCKETS - the websocket value is added here, and registers the urlpatterns from the app routing.py
application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            apps.chatter.routing.websocket_urlpatterns
        )
    )
})