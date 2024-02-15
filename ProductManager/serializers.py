from rest_framework import serializers
from .models import FoodEntity,RestaurantEntity,TypeFoodEntity,ToppingEntity

class FoodEntitySerializer(serializers.ModelSerializer):
    nameRestaurantFood = serializers.CharField(source='restaurant_entity.restaurant_name')
    foodName=serializers.CharField(source='food_name')
    imgFood = serializers.CharField(source='img_food')
    createBy = serializers.CharField(source='create_by')
    createAt = serializers.DateTimeField(source='create_date')
    quantityPurchased = serializers.SerializerMethodField()
    distance = serializers.CharField(source='restaurant_entity.distance')
    typeFoodEntityId = serializers.IntegerField(source='type_food_entity.id')
    restaurantEntityId = serializers.IntegerField(source='restaurant_entity.id')
    nameType = serializers.CharField(source='type_food_entity.name_type')
    toppingList= serializers.SerializerMethodField()
  
    class Meta:
        model = FoodEntity
        fields = ['id', 'foodName', 'price', 'detail', 'nameRestaurantFood', 'imgFood',
                  'createBy', 'createAt', 'quantityPurchased', 'typeFoodEntityId',
                  'restaurantEntityId', 'status', 'distance','toppingList', 'nameType']

    def get_quantityPurchased(self, obj):
        return obj.quantity_purchased if obj.quantity_purchased is not None else ''
    def get_toppingList(self, obj):
        toppings = ToppingEntity.objects.filter(food_entity__restaurant_entity_id=obj.id)
        serializer = ToppingEntitySerializer(toppings, many=True)
        return serializer.data


class RestaurantEntitySerializer(serializers.ModelSerializer):
    restaurantName = serializers.CharField(source='restaurant_name')
    quantitySold = serializers.IntegerField(source='quantity_sold')
    timeStart = serializers.CharField(source='time_start')
    timeClose = serializers.CharField(source='time_close')
    imgRes = serializers.CharField(source='img_res')

    class Meta:
        model = RestaurantEntity
        fields = ['id', 'restaurantName', 'quantitySold', 'timeStart', 'timeClose',
                  'distance', 'imgRes', 'time', 'detail', 'star']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['time'] = instance.time if instance.time is not None else None
        return ret

class TypeFoodSerializer(serializers.ModelSerializer):
    nameType=  serializers.CharField(source='name_type')
    imgType=  serializers.CharField(source='img_type')
    class Meta:
        model = TypeFoodEntity
        fields = ['id', 'nameType','imgType']
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