from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import VoucherEntitySerializer,BillSerializer
# Create your views here.
class CreateBillView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = BillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)