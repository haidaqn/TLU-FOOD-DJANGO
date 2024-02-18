from django.urls import path
from .views import RegistrationAPIView,LoginAPIView,Welcome,AccountApiView,VoucherAPIView,UpdateInfoUserAPIView,FinalChangeInfoUserAPI
urlpatterns = [
    path('register', RegistrationAPIView.as_view(), name='register'),
    path('login', LoginAPIView.as_view(), name='login'),

    path('hello',Welcome.as_view()),
    path('paging-account',AccountApiView.as_view(),name='paing-account'),
    path('update-info-user/<int:pk>',UpdateInfoUserAPIView.as_view(),name='update-info'),
    path('final-update-info-user/<int:otp>',FinalChangeInfoUserAPI.as_view(),name='final-update-info'),
    
    #voucher
    
    path('paging-voucher',VoucherAPIView.as_view(),name='paing-voucher'),
    path('paging-voucher/<int:pk>/',VoucherAPIView.as_view(),name='paing-voucher-path')
    
]