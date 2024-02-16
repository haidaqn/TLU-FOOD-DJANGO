from django.db import models


# Create your models here.
class TypeFoodEntity(models.Model):
    id = models.AutoField(primary_key=True)
    create_by = models.CharField(max_length=255)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(max_length=255, null=True, default=None)
    modified_date = models.DateTimeField(null=True, default=None)
    status = models.BooleanField()
    img_type = models.CharField(max_length=255)
    name_type = models.CharField(max_length=255)
    class Meta:
        db_table = 'type_food_entity'
    
    def __str__(self):
        return self.id

class RestaurantEntity(models.Model):
    id = models.AutoField(primary_key=True)
    create_by = models.CharField(max_length=255)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.CharField(max_length=255, null=True, default=None)
    modified_date = models.DateTimeField(null=True, default=None)
    status = models.BooleanField(default=True)
    address = models.CharField(max_length=255)
    detail = models.CharField(max_length=255)
    distance = models.FloatField()
    img_res = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    quantity_sold = models.IntegerField(null=True)
    restaurant_name = models.CharField(max_length=255)
    star = models.FloatField(null=True, default=None)
    time = models.IntegerField(null=True, default=None)
    time_close = models.CharField(max_length=255)
    time_start = models.CharField(max_length=255)
    class Meta:
        db_table = 'restaurant_entity'
    
    def __str__(self):
        return str(self.id)



class FoodEntity(models.Model):
    id = models.AutoField(primary_key=True)
    create_by = models.CharField(max_length=255)
    create_date = models.DateTimeField()
    modified_by = models.CharField(max_length=255, null=True, default=None)
    modified_date = models.DateTimeField(null=True, default=None)
    status = models.BooleanField(default=True)
    detail = models.CharField(max_length=255)
    food_name = models.CharField(max_length=255)
    img_food = models.CharField(max_length=255)
    price = models.IntegerField()
    quantity_purchased = models.IntegerField(null=True)
    restaurant_entity = models.ForeignKey(RestaurantEntity, on_delete=models.CASCADE)
    star = models.FloatField(null=True, default=None)
    type_food_entity = models.ForeignKey(TypeFoodEntity, on_delete=models.CASCADE)
  
    class Meta:
        db_table = 'food_entity'
    
    def __str__(self):
        return self.id
    
    def update_quantity_purchased(self, order_status, quantity):
        if order_status == 'DELIVERED':
            self.quantity_purchased = quantity
            self.save()
            
    @classmethod
    def update_restaurant_quantity_sold(cls, food_entity):
        # Tính tổng số lượng đã bán của cửa hàng dựa trên tổng số lượng mua của các món ăn của cửa hàng đó
        total_quantity_sold = cls.objects.filter(restaurant_entity=food_entity.restaurant_entity).aggregate(models.Sum('quantity_purchased'))['quantity_purchased__sum']
        if total_quantity_sold is None:
            total_quantity_sold = 0
        
        # Cập nhật trường quantity_sold của cửa hàng
        restaurant = food_entity.restaurant_entity
        restaurant.quantity_sold = total_quantity_sold
        restaurant.save()
class ToppingEntity(models.Model):
    id = models.AutoField(primary_key=True)
    create_by = models.CharField(max_length=255)
    create_date = models.DateTimeField()
    modified_by = models.CharField(max_length=255)
    modified_date = models.DateTimeField()
    status = models.BooleanField()
    food_entity = models.ForeignKey(FoodEntity, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    restaurant_entity = models.ForeignKey(RestaurantEntity, on_delete=models.CASCADE)

    class Meta:
        db_table = 'topping_entity'
    
    def __str__(self):
        return str(self.id)