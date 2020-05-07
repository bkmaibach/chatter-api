from channels.auth import AuthMiddlewareStack
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
import urllib.parse
import channels.db.database_sync_to_async

@database_sync_to_async
def get_token(token_string):
    return Token.objects.get(key=token_key)

class TokenAuthMiddleware:
    """
    Token authorization middleware for Django Channels 2
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        # import pdb; pdb.set_trace()
        # scope = request['scope']
        print(type(scope))
        for key, value in scope.items() :
            print (key, value)
        print('MESSAGE: ' + str(scope))
        headers = dict(scope['headers'])
        query_string_field = scope['query_string'].decode()
        if query_string_field:
            try:
                token_name, token_key_encoded = query_string_field.split('=')
                token_key = urllib.parse.unquote(token_key_encoded)
                print(token_key)
                if token_name == 'token':
                    get_token(token_key)
                    scope['user'] = token.user
                    close_old_connections()
            except Token.DoesNotExist:
                scope['user'] = AnonymousUser()
        return self.inner(scope)

TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))