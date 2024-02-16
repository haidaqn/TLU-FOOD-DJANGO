from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import VoucherEntity
from .serializers import VoucherEntitySerializer,BillSerializer
# Create your views here.
class VoucherEntityApiView(APIView):
    def get(self, request):
        vouchers = VoucherEntity.objects.all()
        serializer = VoucherEntitySerializer(vouchers, many=True)
        return Response({"data":serializer.data})
    
class CreateBillView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = BillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)