from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from apps.chatter.middleware import TokenAuthMiddlewareStack
import apps.chatter.routing

# WEBSOCKETS - the websocket value is added here, and registers the urlpatterns from the app routing.py
application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': TokenAuthMiddlewareStack(
        URLRouter(
            apps.chatter.routing.websocket_urlpatterns
        )
    )
})