from django.urls import path
from .views import RandomFoodAPIView,RandomResAPIView,AllTypeFoodApiView,ResDetailApiView,ResApiView,FoodApiView,FoodByTypeApiView,TypeFoodApiView
urlpatterns = [
    path('rec-food', RandomFoodAPIView.as_view(), name='rec-food'),
    path('rec-res', RandomResAPIView.as_view(), name='rec-rec'),
    path('all-type', AllTypeFoodApiView.as_view(), name='all-type'),
    
    
    # paging
    path('paging-res', ResApiView.as_view(), name='paging-res'),
    path('paging-res/<int:pk>/', ResApiView.as_view(), name='paging-res-path'),
    # path('paging-food', FoodApiView.as_view(), name='paging-food'),
    
    path('paging-food-type/<int:id_type>', FoodByTypeApiView.as_view(), name='paging-food'),
    
    path('paging-type-food', TypeFoodApiView.as_view(), name='paging-type-food'),
    path('paging-type-food/<int:pk>/', TypeFoodApiView.as_view(), name='paging-type-food-path'),
    
    
    path('paging-food/', FoodApiView.as_view(), name='paging-food-query'),
    path('paging-food/<int:pk>/', FoodApiView.as_view(), name='paging-food-path'),
    
    #detail
    path('detail-res/<int:res_id>/', ResDetailApiView.as_view(), name='detail-res'),

]