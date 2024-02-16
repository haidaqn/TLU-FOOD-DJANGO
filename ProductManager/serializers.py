from rest_framework import serializers
from .models import FoodEntity,RestaurantEntity,TypeFoodEntity,ToppingEntity

class FoodEntitySerializer(serializers.ModelSerializer):
    foodName=serializers.CharField(source='food_name')
    imgFood = serializers.CharField(source='img_food')
    createBy = serializers.CharField(source='create_by')
    createAt = serializers.DateTimeField(source='create_date')
    quantityPurchased = serializers.SerializerMethodField()
    typeFoodEntityId = serializers.IntegerField(source='type_food_entity.id')
    restaurantEntityId = serializers.IntegerField(source='restaurant_entity.id')
    toppingList= serializers.SerializerMethodField()
    distance = serializers.CharField(source='restaurant_entity.distance')
    nameType = serializers.CharField(source='type_food_entity.name_type')
    nameRestaurantFood = serializers.CharField(source='restaurant_entity.restaurant_name')
    star = serializers.FloatField()
  
    class Meta:
        model = FoodEntity
        fields = ['id', 'foodName', 'price', 'detail', 'nameRestaurantFood', 'imgFood',
                  'createBy', 'createAt', 'quantityPurchased', 'typeFoodEntityId',
                  'restaurantEntityId', 'status', 'distance','toppingList', 'nameType','star']
        # fields = ['id', 'foodName', 'price', 'detail', 'imgFood',
        #           'createBy', 'createAt', 'quantityPurchased', 'typeFoodEntityId',
        #           'restaurantEntityId', 'status', 'toppingList']

    def get_quantityPurchased(self, obj):
        return obj.quantity_purchased if obj.quantity_purchased is not None else ''
    def get_toppingList(self, obj):
        toppings = ToppingEntity.objects.filter(food_entity__restaurant_entity_id=obj.id)
        serializer = ToppingEntitySerializer(toppings, many=True)
        return serializer.data
  
    def create(self, validated_data):
        # Trích xuất thông tin từ validated_data
        restaurant_data = validated_data.pop('restaurant_entity', None)
        type_food_data = validated_data.pop('type_food_entity', None)

        # Truy vấn hoặc tạo mới đối tượng RestaurantEntity
        restaurant_entity = None
        if restaurant_data:
            restaurant_id = restaurant_data.get('id')
            restaurant_name = restaurant_data.get('restaurant_name')
            # Truy vấn hoặc tạo mới đối tượng RestaurantEntity
            restaurant_entity, created = RestaurantEntity.objects.get_or_create(
                id=restaurant_id,
                defaults={'restaurant_name': restaurant_name}
            )

        # Truy vấn hoặc tạo mới đối tượng TypeFoodEntity
        type_food_entity = None
        if type_food_data:
            type_food_id = type_food_data.get('id')
            type_food_name = type_food_data.get('name_type')
            # Truy vấn hoặc tạo mới đối tượng TypeFoodEntity
            type_food_entity, created = TypeFoodEntity.objects.get_or_create(
                id=type_food_id,
                defaults={'name_type': type_food_name}
            )
            
        # Tạo mới một đối tượng FoodEntity
        food_entity = FoodEntity.objects.create(
            **validated_data,
            restaurant_entity=restaurant_entity,
            type_food_entity=type_food_entity
        )
        
        food_entity.status = True
        
        food_entity.save()

        return food_entity

    def delete_multiple(self, ids):
        # Xóa các bản ghi dựa trên danh sách các id được cung cấp
        deleted_count, _ = FoodEntity.objects.filter(id__in=ids).delete()
        return deleted_count
    
    def update(self, instance, validated_data):
        # Cập nhật các trường thông thường
        instance.food_name = validated_data.get('food_name', instance.food_name)
        instance.price = validated_data.get('price', instance.price)
        instance.detail = validated_data.get('detail', instance.detail)
    
        # Cập nhật restaurant_entity
        restaurant_data = validated_data.pop('restaurant_entity', None)
        if restaurant_data:
            restaurant_id = restaurant_data.get('id')
            restaurant_name = restaurant_data.get('restaurant_name')
            restaurant_entity, created = RestaurantEntity.objects.get_or_create(
                id=restaurant_id,
                defaults={'restaurant_name': restaurant_name}
            )
            instance.restaurant_entity = restaurant_entity

        # Cập nhật type_food_entity
        type_food_data = validated_data.pop('type_food_entity', None)
        if type_food_data:
            type_food_id = type_food_data.get('id')
            type_food_name = type_food_data.get('name_type')
            type_food_entity, created = TypeFoodEntity.objects.get_or_create(
                id=type_food_id,
                defaults={'name_type': type_food_name}
            )
            instance.type_food_entity = type_food_entity

        instance.save()
        return instance
    

class RestaurantEntitySerializer(serializers.ModelSerializer):
    restaurantName = serializers.CharField(source='restaurant_name')
    quantitySold = serializers.IntegerField(source='quantity_sold')
    timeStart = serializers.CharField(source='time_start')
    timeClose = serializers.CharField(source='time_close')
    imgRes = serializers.CharField(source='img_res')
    phoneNumber = serializers.CharField(source='phone_number')
    star = serializers.FloatField()
    address = serializers.CharField()

    class Meta:
        model = RestaurantEntity
        fields = ['id', 'restaurantName', 'quantitySold', 'timeStart', 'timeClose',
                  'distance', 'imgRes', 'time', 'detail', 'star', 'phoneNumber','address']  # Bao gồm trường 'phoneNumber'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['time'] = instance.time if instance.time is not None else None
        return ret
    
    def create(self, validated_data):
        # Tạo mới một đối tượng FoodEntity
        res_entity = RestaurantEntity.objects.create(
            **validated_data,
        )
        res_entity.status = True
        
        res_entity.save()

        return res_entity
    
    def delete_multiple(self, ids):
        deleted_count, _ = RestaurantEntity.objects.filter(id__in=ids).delete()
        return deleted_count

class TypeFoodSerializer(serializers.ModelSerializer):
    nameType=  serializers.CharField(source='name_type')
    imgType=  serializers.CharField(source='img_type')
    status = serializers.BooleanField()
    class Meta:
        model = TypeFoodEntity
        fields = ['id', 'nameType','imgType','status']
    
    def create(self, validated_data):
            
        # Tạo mới một đối tượng FoodEntity
        type_food_entity = TypeFoodEntity.objects.create(
            **validated_data,
        )
        
        type_food_entity.status = True
        
        type_food_entity.save()

        return type_food_entity
        
    def delete_multiple(self, ids):
        deleted_count, _ = TypeFoodEntity.objects.filter(id__in=ids).delete()
        return deleted_count
    
    def update(self, instance, validated_data):
        instance.name_type = validated_data.get('name_type', instance.name_type)
        instance.img_type = validated_data.get('img_type', instance.img_type)
        instance.save()
        return instance
        
        
class ToppingEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ToppingEntity
        fields = ['id', 'create_date', 'status', 'name', 'price']
class ResDetailDataSerializer(serializers.ModelSerializer):

    toppingList = serializers.SerializerMethodField()
    foods = serializers.SerializerMethodField()
    class Meta:
        model = RestaurantEntity
        fields = ['id', 'create_date', 'status', 'restaurant_name', 'quantity_sold', 'distance', 'star', 'time_start', 'time_close', 'detail', 'img_res','toppingList', 'foods']
    
    def get_toppingList(self, obj):
        toppings = ToppingEntity.objects.filter(food_entity__restaurant_entity_id=obj.id)
        serializer = ToppingEntitySerializer(toppings, many=True)
        return serializer.data

    def get_foods(self, obj):
        foods = FoodEntity.objects.filter(restaurant_entity_id=obj.id)
        serializer = FoodEntitySerializer(foods, many=True)
        return serializer.data