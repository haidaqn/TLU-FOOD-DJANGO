from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import FoodEntity,RestaurantEntity,TypeFoodEntity
from .serializers import FoodEntitySerializer,RestaurantSerializer,TypeFoodSerializer
import random

class RandomFoodAPIView(APIView):
    def get(self, request):
        # Lấy tất cả các món ăn từ cơ sở dữ liệu
        all_foods = FoodEntity.objects.all()
        
        # Chọn ngẫu nhiên 10 món ăn từ danh sách
        random_foods = random.sample(list(all_foods), 10)
        
        # Serialize danh sách món ăn
        serializer = FoodEntitySerializer(random_foods, many=True)
        
        # Trả về dữ liệu JSON của 10 món ăn ngẫu nhiên
        return Response({"data":serializer.data,"message":"Lấy dữ liệu thành công"})
class RandomResAPIView(APIView):
    def get(self, request):
        # Lấy tất cả các món ăn từ cơ sở dữ liệu
        all_ress = RestaurantEntity.objects.all()
        
        # Chọn ngẫu nhiên 10 món ăn từ danh sách
        random_ress = random.sample(list(all_ress), 10)
        
        # Serialize danh sách món ăn
        serializer = RestaurantSerializer(random_ress, many=True)
        
        # Trả về dữ liệu JSON của 10 món ăn ngẫu nhiên
        return Response({"data":serializer.data,"message":"Lấy dữ liệu thành công"})

class AllTypeFoodApiView(APIView):
    def get(self,request):
        all_types = TypeFoodEntity.objects.all()
        serializer = TypeFoodSerializer(all_types, many=True)
        return Response({"data":serializer.data,"message":"Lấy dữ liệu thành công"})