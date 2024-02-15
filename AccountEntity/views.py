from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import RegisterSerializer, LoginSerializer, AccountEntitySerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import AccountEntity
from rest_framework.pagination import PageNumberPagination

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


class ProtectedAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # This view is protected and requires authentication
        return Response({'message': 'You are authenticated'})


class InvoiceAPIView(APIView):
    pass

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