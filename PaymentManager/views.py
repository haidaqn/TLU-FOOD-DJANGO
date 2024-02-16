from rest_framework.views import APIView
from rest_framework.response import Response
from .models import VoucherEntity
from .serializers import VoucherEntitySerializer
# Create your views here.
class VoucherEntityApiView(APIView):
    def get(self, request):
        vouchers = VoucherEntity.objects.all()
        serializer = VoucherEntitySerializer(vouchers, many=True)
        return Response({"data":serializer.data})