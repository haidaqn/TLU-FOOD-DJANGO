from django.urls import path
from .views import VoucherEntityApiView

urlpatterns = [
    path('vouchers', VoucherEntityApiView.as_view(), name='voucher-list'),
    
]
