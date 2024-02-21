from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .serializers import BillSerializer
from AccountEntity.models import AccountEntity
from .models import BillEntity,ORDER_STATUS_CHOICES
# Create your views here.
class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'pageSize'
    page_query_param ='pageIndex'   
    
class BillApiView(APIView):
    serializer_class = BillSerializer
    pagination_class = CustomPageNumberPagination
    
    def get_queryset(self, user_id, order_status=None):
        queryset = BillEntity.objects.filter(create_by_id=user_id)
        if order_status is not None: # In ra giá trị order_status_value để kiểm tra
            for choice_value, choice_name in ORDER_STATUS_CHOICES:
                if choice_name == order_status:
                    queryset = queryset.filter(order_status=choice_value)
                    return queryset
            # Nếu không tìm thấy trạng thái phù hợp, trả về queryset rỗng
            return queryset.none()
        return queryset
    def get_queryset_all(self, order_status=None):
        queryset = BillEntity.objects.all()
        print(queryset)
        if order_status is not None: # In ra giá trị order_status_value để kiểm tra
            for choice_value, choice_name in ORDER_STATUS_CHOICES:
                if choice_name == order_status:
                    queryset = queryset.filter(order_status=choice_value)
                    return queryset
            # Nếu không tìm thấy trạng thái phù hợp, trả về queryset rỗng
            return queryset.none()
        return queryset
    def get(self,request):
        user_id = request.user_id
        user=AccountEntity.objects.get(id=user_id)
        order_status = request.query_params.get('orderStatus')
        queryset=""
        if(user.is_staff):
           queryset=self.get_queryset(user_id=user_id, order_status=order_status)
        else:
            queryset=self.get_queryset_all(order_status=order_status)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(page, many=True)
        
        total_rows = queryset.count()  # Tính tổng số hàng của toàn bộ dữ liệu
        response_data = {
            'totalRow': total_rows,
            'data': serializer.data
        }
        return Response(response_data)
    def patch(self, request):
        bill_id = request.query_params.get('id')
        if not bill_id:
            return Response({"message": "Bill id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            bill = BillEntity.objects.get(pk=bill_id)
        except BillEntity.DoesNotExist:
            return Response({"message": "Bill not found"}, status=status.HTTP_404_NOT_FOUND)
        if(bill.order_status==1):
            bill.order_status = 4  # Cập nhật trạng thái của đơn hàng thành CANCELED
            bill.save()
            return Response({"message:Hủy đơn thành công"})
        return Response({"message:Hủy đơn thất bại"}, status=status.HTTP_400_BAD_REQUEST)
class BillDetailApiView(APIView):
    def get(self,request,bill_id):
        if not bill_id:
            return Response({"message": "Bill id is required"}, status=status.HTTP_400_BAD_REQUEST)
        bill=BillEntity.objects.get(id=bill_id)
        serializer=BillSerializer(bill)
        return Response({'data':serializer.data},status=status.HTTP_200_OK)
    def patch(self, request,bill_id):
        # Lấy thông tin từ query parameters
        order_status = request.query_params.get('orderStatus')

        # Kiểm tra xem orderStatus và id đã được cung cấp chưa
        if not order_status or not bill_id:
            return Response({"message": "Both orderStatus and id are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Tìm và cập nhật hóa đơn
            bill = BillEntity.objects.get(pk=bill_id)
            order_status_val = None
            for choice_value, choice_name in ORDER_STATUS_CHOICES:
                if choice_name == order_status:
                    order_status_val = choice_value
                    break
            bill.order_status = order_status_val
            bill.save()
            return Response({"message": "Bill updated successfully"}, status=status.HTTP_200_OK)
        except BillEntity.DoesNotExist:
            return Response({"message": "Bill not found"}, status=status.HTTP_404_NOT_FOUND)
