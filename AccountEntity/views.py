from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import RegisterSerializer, LoginSerializer, AccountEntitySerializer,VoucherSerializer,UpdateUserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import AccountEntity,VoucherEntity
from rest_framework.pagination import PageNumberPagination
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.core.mail import send_mail
from rest_framework.response import Response
import random
from django.http import HttpResponse
from django.conf import settings
from django.http import JsonResponse
class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'pageSize'
    page_query_param ='pageIndex' 

# Create your views here.
class Welcome(APIView):
    def get(self, request):
        return Response("Chào mừng đến với TLU FOOD")
class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            user_serializer = AccountEntitySerializer(user)  
            return Response({
                'message':'Tạo tài khoản thành công',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'data': user_serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            user = AccountEntity.objects.authenticate(
                request, username=username, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                user_serializer = AccountEntitySerializer(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'data': user_serializer.data
                })
            else:
                return Response({'message': 'Tài khoản hoặc mật khẩu không chính xác'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class InvoiceAPIView(APIView):
    pass


class VoucherAPIView(APIView):
    serializer_class = VoucherSerializer
    pagination_class = CustomPageNumberPagination
    def get_queryset(self):
        return VoucherEntity.objects.all().order_by('id')
    
    def get(self, request, *args, **kwargs):
        if 'pageSize' in request.query_params and 'pageIndex' in request.query_params:
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
        else :
            pk = kwargs.get('pk')
            if pk is not None:
                res = VoucherEntity.objects.get(pk=pk)
                serializer = self.serializer_class(res)
                return Response(serializer.data)
            else:
                return Response({"message": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
    
    
    def post(self, request, *args, **kwargs):
        serializer = VoucherSerializer(data=request.data)
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
    
    
    def put(self, request, *args, **kwargs):
        # Lấy id từ đường dẫn
        food_id = kwargs.get('pk')
        try:
            food = VoucherEntity.objects.get(id=food_id)
            serializer = self.serializer_class(food, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except VoucherEntity.DoesNotExist:
            return Response({"message": "voucher not found"}, status=status.HTTP_404_NOT_FOUND)
    

class AccountApiView(APIView):
    serializer_class = AccountEntitySerializer
    pagination_class = CustomPageNumberPagination
    def get_queryset(self):
        return AccountEntity.objects.all().order_by('id')
    
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
class InfoApiView(APIView):
    def patch(self, request, *args, **kwargs):
        account_entity = AccountEntity.objects.get(id=request.user_id)
        serializer = AccountInfoSerializer(account_entity, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UpdateInfoUserAPIView(APIView):
    def post(self, request, pk):
        try:
            user = AccountEntity.objects.get(pk=pk)
        except AccountEntity.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        def generate_random_numbers():
            random_numbers = [random.randint(0, 9) for _ in range(6)]
            return ''.join(map(str, random_numbers))

        # Sử dụng hàm
        otp = generate_random_numbers()
        data_user = {
            'data': request.data,
            'otp': otp,
            'idUser': pk
        }
        # response = HttpResponse("Welcome TLU-FOOD.")  
        cookie_data = json.dumps(data_user) 
        response = Response({"message": "OTP sent successfully", "status": status.HTTP_200_OK})
        response.set_cookie('data-update', cookie_data)
        email_message = f'Mã OTP của bạn là = {otp} xin vui lòng không chia sẻ với ai !'
        send_mail(
            'OTP CHANGE INFO USER AT TLU-FOOD',
            email_message,
            settings.DEFAULT_FROM_EMAIL,
            [request.data.get('email')],
            fail_silently=False,
        )
        return response

            
class FinalChangeInfoUserAPI(APIView) :
    def post(self, request, otp):
        cookie = request.COOKIES.get('data-update')
        if not cookie:
            return JsonResponse({"error": "Cookie 'data-update' not found"}, status=status.HTTP_404_NOT_FOUND)
        
        data_change = json.loads(cookie)
        print(data_change.get('otp'))
        print(otp)
        if str(otp) != str(data_change.get('otp')):
            response = JsonResponse({"error": "OTP does not match"}, status=status.HTTP_400_BAD_REQUEST)
            response.delete_cookie('data-update')
            return response
        
        try:
            user = AccountEntity.objects.get(pk=data_change.get('idUser'))
        except AccountEntity.DoesNotExist:
            response = JsonResponse({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            response.delete_cookie('data-update')
            return response
        
        serializer = UpdateUserSerializer(user, data=data_change.get('data'), partial=True)
        if serializer.is_valid():
            serializer.save()
            response = JsonResponse(serializer.data)
            response.delete_cookie('data-update')
            return response
        
        response = JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        response.delete_cookie('data-update')
        return response
           