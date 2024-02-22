# middleware.py
from channels.middleware import BaseMiddleware
from urllib.parse import parse_qs
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from django.http import JsonResponse
import re
class JWTAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        query_params = parse_qs(scope['query_string'])
        token = query_params.get(b'token', [])[0].decode('utf-8') 
        if token:
            try:
                access_token = AccessToken(token)
                user_id = access_token.payload.get('user_id')
                scope['user_id'] = user_id
            except Exception as e:
                print(e)
                scope['user_id'] = AnonymousUser()
        else:
            scope['user'] = AnonymousUser()
        
        return await super().__call__(scope, receive, send)


class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
         # Danh sách các path mà middleware sẽ bỏ qua việc kiểm tra token
        self.exclude_path_patterns = [

            r'^/auth/hello$',
            r'^/auth/login$',
            r'^/auth/register$',
            r'^/auth/forgot-password/\w+$',
            r'^/prod/paging-food-type/\d+$',        
            r'^/prod/search-food/\d+$',
            r'^/prod/paging-res$',
            r'^/prod/paging-food$',
            r'^/prod/detail-res/\d+$',
            r'^/prod/search-food',
            r'^/prod/all-type$',
            r'^/prod/rec-res$',
            r'^/prod/rec-food$',
        ]

    def __call__(self, request):
        jwt_token = request.headers.get('Authorization', None)
        print(jwt_token)
        path = request.path
        for pattern in self.exclude_path_patterns:
            if re.match(pattern, path):
                # Nếu đường dẫn trùng khớp, bỏ qua việc kiểm tra token và tiếp tục xử lý request
                response = self.get_response(request)
                return response


        if jwt_token:
            jwt_token=jwt_token.split(" ")[1]
            try:
                access_token = AccessToken(jwt_token)
                user_id = access_token.payload.get('user_id')
                request.user_id = user_id
                print("User:",user_id)
            except Exception as e:
                print("Error:", e)
                request.user_id = None
                return JsonResponse({'error': 'Token is invalid or expired'}, status=401)
        else:
                # Không có token được cung cấp, trả về mã trạng thái 401
                return JsonResponse({'error': 'Token is required'}, status=401)

        response = self.get_response(request)
        return response
