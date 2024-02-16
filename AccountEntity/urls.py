from django.urls import path
from .views import RegistrationAPIView,LoginAPIView,Welcome,AccountApiView
urlpatterns = [
    path('register', RegistrationAPIView.as_view(), name='register'),
    path('login', LoginAPIView.as_view(), name='login'),

    path('hello',Welcome.as_view()),
    path('paging-account',AccountApiView.as_view(),name='paing-account')
]