from rest_framework import serializers
from .models import BillDetailEntity,BillEntity
class BillDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillDetailEntity
        fields = ['id', 'create_by', 'create_date', 'quantity', 'item', 'food_entity_id']

class BillSerializer(serializers.ModelSerializer):
    bill_details = BillDetailSerializer(many=True, read_only=True)

    class Meta:
        model = BillEntity
        fields = ['id', 'create_by', 'create_date', 'modified_by', 'modified_date', 'status', 'finish_date', 'order_by', 'order_status', 'total_amount', 'account_entity', 'name_res', 'finish_time', 'ship_fee', 'code', 'note', 'bill_details']
