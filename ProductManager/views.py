from rest_framework import status
from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import FoodEntity, RestaurantEntity, TypeFoodEntity
from .serializers import FoodEntitySerializer, RestaurantEntitySerializer, TypeFoodSerializer, ResDetailDataSerializer
import random

class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'pageSize'
    page_query_param ='pageIndex'   
    
class RandomFoodAPIView(APIView):
    def get(self, request):
        # Lấy tất cả các món ăn từ cơ sở dữ liệu
        all_foods = FoodEntity.objects.all()
        
        # Chọn ngẫu nhiên 10 món ăn từ danh sách
        random_foods = random.sample(list(all_foods), 10)
        
        # Serialize danh sách món ăn
        serializer = FoodEntitySerializer(random_foods, many=True)
        
        # Trả về dữ liệu JSON của 10 món ăn ngẫu nhiên
        return Response({"data": serializer.data, "message": "Lấy dữ liệu thành công"})

class RandomResAPIView(APIView):
    def get(self, request):
        # Lấy tất cả các nhà hàng từ cơ sở dữ liệu
        all_ress = RestaurantEntity.objects.all()
        
        # Chọn ngẫu nhiên 10 nhà hàng từ danh sách
        random_ress = random.sample(list(all_ress), 10)
        
        # Serialize danh sách nhà hàng
        serializer = RestaurantEntitySerializer(random_ress, many=True)
        
        # Trả về dữ liệu JSON của 10 nhà hàng ngẫu nhiên
        return Response({"data": serializer.data, "message": "Lấy dữ liệu thành công"}, status=status.HTTP_200_OK)

class AllTypeFoodApiView(APIView):
    def get(self,request):
        all_types = TypeFoodEntity.objects.all()
        serializer = TypeFoodSerializer(all_types, many=True)
        return Response({"data":serializer.data,"message":"Lấy dữ liệu thành công"}, status=status.HTTP_200_OK)
    
class ResDetailApiView(APIView):
    def get(self, request, res_id):
        restaurant = RestaurantEntity.objects.get(id=res_id)
        serializer = ResDetailDataSerializer(restaurant)
        print(serializer)
        return Response({"data":serializer.data,"message":"Lấy dữ liệu thành công"}, status=status.HTTP_200_OK)


class ResApiView(APIView):
    serializer_class = RestaurantEntitySerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return RestaurantEntity.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(page, many=True)
        
        total_rows = queryset.count()  # Tính tổng số hàng của toàn bộ dữ liệu
        response_data = {
            'totalRow': total_rows,
            'data': serializer.data
        }
        return Response(response_data)
    
class FoodApiView(APIView):
    serializer_class = FoodEntitySerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return FoodEntity.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(page, many=True)
        
        total_rows = queryset.count()  # Tính tổng số hàng của toàn bộ dữ liệu
        response_data = {
            'totalRow': total_rows,
            'data': serializer.data
        }
        return Response(response_data)
    
class FoodByTypeApiView(APIView):
    serializer_class = FoodEntitySerializer

    def get_queryset(self,id_type):
        return FoodEntity.objects.filter(type_food_entity_id=id_type)

    def get(self, request, id_type):
        queryset = self.get_queryset(id_type)
        serializer = FoodEntitySerializer(queryset, many=True)
        response_data = {
            'nameType':TypeFoodEntity.objects.get(id=id_type).name_type,
            'data': serializer.data
        }
        return Response(response_data)
    
class SearchFoodApiView(APIView):
    def get(self, request):
        search_string = request.query_params.get('searchString', '')
        if search_string:
            foods = FoodEntity.objects.filter(food_name__icontains=search_string)
            serializer = FoodEntitySerializer(foods, many=True)
            return Response({"data":serializer.data})
        else:
            return Response({'message': 'Vui lòng nhập chuỗi tìm kiếm.'}, status=400)