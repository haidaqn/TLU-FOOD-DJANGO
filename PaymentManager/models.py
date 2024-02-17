from django.db import models
from AccountEntity.models import AccountEntity
from ProductManager.models import FoodEntity
# Create your models here.
from django.db import models
from django.utils import timezone

ORDER_STATUS_CHOICES = [
        (1, 'PENDING'),
        (2, 'PROCESSING'),
        (3, 'DELIVERED'),
        (4, 'CANCELD'),
    ]
class BillEntity(models.Model):
    
    id = models.AutoField(primary_key=True)
    create_by =models.ForeignKey(AccountEntity,null=True ,on_delete=models.SET_NULL, related_name='bills_created')
    create_date = models.DateTimeField(default=timezone.now)
    modified_by =models.ForeignKey(AccountEntity,null=True ,on_delete=models.SET_NULL, related_name='bills_modified')
    modified_date = models.DateTimeField(null=True)
    finish_date = models.DateTimeField(null=True) 
    order_status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES,default=1)
    total_amount = models.BigIntegerField()
    account_entity = models.ForeignKey(AccountEntity,null=True ,on_delete=models.SET_NULL)
    name_res = models.CharField(max_length=255)
    finish_time = models.CharField(max_length=255)
    ship_fee = models.IntegerField(default=0)
    code = models.CharField(max_length=255)
    note = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'bill_entity'
    
    def __str__(self):
        return f"Bill id {self.id}"
    def save(self, *args, **kwargs):
        # Cập nhật giá trị modified_date mỗi khi lưu thay đổi vào cơ sở dữ liệu
        self.modified_date = timezone.now()
        super().save(*args, **kwargs)
    
class BillDetailEntity(models.Model):
    id = models.AutoField(primary_key=True)
    quantity = models.IntegerField()
    item = models.CharField(max_length=255)
    bill_entity_id = models.ForeignKey(BillEntity, on_delete=models.CASCADE)
    food_entity_id = models.ForeignKey(FoodEntity, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'bill_detail_entity'
    
    def __str__(self):
        return self.id
    