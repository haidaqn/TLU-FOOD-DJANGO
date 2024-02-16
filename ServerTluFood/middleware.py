# middleware.py
from channels.middleware import BaseMiddleware

from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken

class JWTAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        if b'authorization' in headers:
            try:
                token = headers[b'authorization'].decode('utf8').split()[1]
                access_token = AccessToken(token)
                user = access_token.user
                scope['user'] = user
            except Exception as e:
                scope['user'] = AnonymousUser()
        return await super().__call__(scope, receive, send)
