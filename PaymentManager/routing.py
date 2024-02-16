# myapp/routing.py
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/checkout/', consumers.CheckoutConsumer.as_asgi()),
]
