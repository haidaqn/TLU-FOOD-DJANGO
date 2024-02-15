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
    
    def post(self, request, *args, **kwargs):
        serializer = FoodEntitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        # Lấy danh sách các id cần xóa từ request.data
        ids_to_delete = request.data
        
        # Tạo một instance của serializer
        serializer = self.serializer_class(data={})
        # Gọi phương thức delete_multiple để xóa các bản ghi
        deleted_count = serializer.delete_multiple(ids_to_delete)
        # Kiểm tra số lượng bản ghi đã bị xóa
        if deleted_count > 0:
            return Response({"message": f"{deleted_count} bản ghi đã được xóa"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "Không có bản ghi nào được xóa"}, status=status.HTTP_404_NOT_FOUND)
    
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
    
    def create(self, request, *args, **kwargs):
        serializer = FoodEntitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class TypeFoodApiView(APIView):
    serializer_class = TypeFoodSerializer
    pagination_class = CustomPageNumberPagination
    
    def get_queryset(self):
        return TypeFoodEntity.objects.all().order_by('id')
    
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
    