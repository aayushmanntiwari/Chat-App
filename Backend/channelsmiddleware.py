from django.db import close_old_connections
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from jwt import decode as jwt_decode
from django.contrib.auth.models import User
from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.conf import settings
from base64 import b64decode

@database_sync_to_async
def get_user(validated_token):
    try:
        user = User.objects.get(id=validated_token["user_id"])
        # return get_user_model().objects.get(id=toke_id)
        #print(f"{user}")
        return user

    except User.DoesNotExist:
        return None

class JwtAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner
    
    async def __call__(self, scope, receive, send):
        close_old_connections()
        token = parse_qs(scope["query_string"].decode("utf8"))["token"][0]
        #print(token)
        try:
            # This will automatically validate the token and raise an error if token is invalid
            UntypedToken(token)
        except (InvalidToken, TokenError) as e:
            # Token is invalid
            print(e)
            return None
        else:
            #print(token)
            decoded_data = jwt_decode(token,settings.SECRET_KEY,algorithms=["HS256"])
            #print(decoded_data['user_id'])
            scope["user"] = await get_user(validated_token=decoded_data)
        return await super().__call__(scope, receive, send)

def JwtAuthMiddlewareStack(inner):
    return JwtAuthMiddleware(AuthMiddlewareStack(inner))
