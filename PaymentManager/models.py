from django.db import models

# Create your models here.
from django.db import models

class VoucherEntity(models.Model):
    id = models.AutoField(primary_key=True)
    create_by = models.CharField(max_length=255)
    create_date = models.DateTimeField()
    modified_by = models.CharField(max_length=255)
    modified_date = models.DateTimeField()
    status = models.BooleanField()
    detail = models.CharField(max_length=255)
    expired = models.DateTimeField()
    quantity = models.IntegerField()
    discount = models.IntegerField()
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=255)

    class Meta:
        db_table = 'voucher_entity'
    
    def __str__(self):
        return self.id