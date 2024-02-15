
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/',include('AccountEntity.urls')),
    path('prod/',include('ProductManager.urls')),
  
]
