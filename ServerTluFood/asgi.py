import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from .middleware import JWTAuthMiddleware
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from PaymentManager.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ServerTluFood.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket':  AuthMiddlewareStack(
        JWTAuthMiddleware(
            URLRouter(
                websocket_urlpatterns
            )
        )
       
    ),
})
