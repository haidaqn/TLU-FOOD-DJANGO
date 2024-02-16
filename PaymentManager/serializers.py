from rest_framework import serializers
from .models import VoucherEntity

class VoucherEntitySerializer(serializers.ModelSerializer):
    createDate = serializers.DateTimeField(source='create_date', format='%Y-%m-%dT%H:%M:%S')
    expired = serializers.DateTimeField(source='expired',format='%Y-%m-%dT%H:%M:%S')

    class Meta:
        model = VoucherEntity
        fields = ['id', 'createDate', 'status', 'discount', 'expired', 'detail', 'code', 'quantity', 'title']
