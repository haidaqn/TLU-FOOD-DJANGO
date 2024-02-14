from django.urls import path
from .views import RandomFoodAPIView,RandomResAPIView,AllTypeFoodApiView
urlpatterns = [
    path('rec-food', RandomFoodAPIView.as_view(), name='rec-food'),
    path('rec-res', RandomResAPIView.as_view(), name='rec-rec'),
    path('all-type', AllTypeFoodApiView.as_view(), name='all-type'),
    
]