from django.urls import path
from .views import (RegistrationAPIView, LoginAPIView, Welcome, AccountApiView, VoucherAPIView, UpdateInfoUserAPIView, FinalChangeInfoUserAPI, 
                    ForgotPasswordAPIView, ChangePasswordAPIView, VoucherCusAPIView,ExtractTextFromImageView)
urlpatterns = [
    path('register', RegistrationAPIView.as_view(), name='register'),
    path('login', LoginAPIView.as_view(), name='login'),

    path('hello', Welcome.as_view()),
    path('paging-account', AccountApiView.as_view(), name='paing-account'),
    path('update-info-user/<int:pk>',
         UpdateInfoUserAPIView.as_view(), name='update-info'),
    path('final-update-info/<int:otp>',
         FinalChangeInfoUserAPI.as_view(), name='final-update-info'),
    path('forgot-password/<str:username>',
         ForgotPasswordAPIView.as_view(), name='forgot-password'),
    path('change-password/<str:username>',
         ChangePasswordAPIView.as_view(), name='change-password'),

    # voucher
    path('vouchers', VoucherCusAPIView.as_view(), name='all-voucher'),
    path('paging-voucher', VoucherAPIView.as_view(), name='paging-voucher'),
    path('paging-voucher/<int:pk>/',
         VoucherAPIView.as_view(), name='paging-voucher-path'),
     path('check_thesv', ExtractTextFromImageView.as_view(), name='detect_text'),
]
