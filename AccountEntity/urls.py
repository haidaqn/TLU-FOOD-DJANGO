from django.urls import path
from .views import RegistrationAPIView,LoginAPIView,ProtectedAPIView,Welcome
urlpatterns = [
    path('register', RegistrationAPIView.as_view(), name='register'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('protected', ProtectedAPIView.as_view(), name='protected'),
    path('hello',Welcome.as_view())
]