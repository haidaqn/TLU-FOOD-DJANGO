# middleware.py
from channels.middleware import BaseMiddleware
from urllib.parse import parse_qs
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken

class JWTAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        query_params = parse_qs(scope['query_string'])
        token = query_params.get(b'token', [])[0].decode('utf-8') 
        if token:
            try:
                access_token = AccessToken(token)
                user = access_token.payload.get('user_id')
                scope['user_id'] = user
            except Exception as e:
                print(e)
                scope['user_id'] = AnonymousUser()
        else:
            scope['user'] = AnonymousUser()
        
        return await super().__call__(scope, receive, send)
