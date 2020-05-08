from urllib.parse import unquote
from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token

# Oh man what?
# To attempt to activate this dumpster fire:
# put TokenAuthMiddlewareStack in place of AuthMiddlewareStack
# In project level routing.py
# Currently gives error that scope['user'] is NoneTypegit reset 
@database_sync_to_async
def get_user(query_string):
    try:
        token_name, token_key_encoded = query_string.split('=')
        token_key = unquote(token_key_encoded)
        if token_name == 'Token':
            token = Token.objects.get(key=token_key)
            print("OBTAINED USER ID" + str(token.user))
            return token.user
    except Token.DoesNotExist:
        return AnonymousUser()

class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return TokenAuthMiddlewareInstance(scope, self)

class TokenAuthMiddlewareInstance:
    """
    Yeah, this is black magic:
    https://github.com/django/channels/issues/1399
    """
    def __init__(self, scope, middleware):
        self.middleware = middleware
        self.scope = dict(scope)
        self.inner = self.middleware.inner

    async def __call__(self, receive, send):
        if not self.scope['user'] is None:
            query_string = self.scope['query_string'].decode()
            if query_string:
                print("OBTAINED QUERY STRING " + query_string)
                self.scope['user'] = await get_user(query_string)
            inner = self.inner(self.scope)
            return await inner(receive, send)
        else:
            print("IT IS NONE!!!")

TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))