from django.urls import path
from .views import BillApiView,BillDetailApiView
urlpatterns = [
    path('bill',BillApiView.as_view(),name='bill'),
    path('detail-bill/<int:bill_id>',BillDetailApiView.as_view(),name='bill-detail')
    
]
