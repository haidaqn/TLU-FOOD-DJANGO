from rest_framework import serializers
from .models import BillDetailEntity,BillEntity
from AccountEntity.serializers import AccountEntitySerializer
from AccountEntity.models import AccountEntity
class BillDetailSerializer(serializers.ModelSerializer):
    foodId = serializers.IntegerField(source='food_entity.id')
    nameFood = serializers.CharField(source='food_entity.food_name')
    priceFood = serializers.CharField(source='food_entity.price')
    nameRes = serializers.CharField(source='food_entity.restaurant_entity.restaurant_name')
    address = serializers.CharField(source='food_entity.restaurant_entity.address')
    
    resId = serializers.IntegerField(source='bill_entity.account_entity_id')

    class Meta:
        model = BillDetailEntity
        fields = ['foodId', 'nameFood', 'priceFood', 'quantity', 'nameRes', 'resId', 'item_list','address']
class BillSerializer(serializers.ModelSerializer):
    voucherResponseBill = serializers.CharField(source='code')
    foodResponseBills = serializers.SerializerMethodField()
    orderStatus= serializers.CharField(source='get_order_status_display')
    accountId=serializers.IntegerField(source="account_entity_id")
    accountName=serializers.CharField(source="account_entity.account_name")
    user=serializers.SerializerMethodField()
    class Meta:
        model = BillEntity
        fields = (
            'id',
            'create_date',
            'orderStatus',
            'accountId',
            'accountName',
            'user',
            'ship_fee',
            'finish_time',
            'total_amount',
            'note',
            'voucherResponseBill',
            'foodResponseBills',
        )

    def get_voucherResponseBill(self, obj):
        # Logic để lấy thông tin voucherResponseBill (nếu có)
        return []  # Thay bằng logic lấy thông tin voucherResponseBill
    def get_user(self,obj):
        serializer = AccountEntitySerializer(obj.account_entity)
        return serializer.data
    def get_foodResponseBills(self, obj):
        # Logic để lấy thông tin foodResponseBills (nếu có)
        # Đây là một ví dụ giả định
        food_bills = BillDetailEntity.objects.filter(bill_entity_id=obj)
        serializer = BillDetailSerializer(food_bills, many=True)
        return serializer.data