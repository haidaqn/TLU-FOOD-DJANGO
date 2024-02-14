from rest_framework import serializers
from .models import FoodEntity,RestaurantEntity,TypeFoodEntity

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

    class Meta:
        model = FoodEntity
        fields = ['id', 'foodName', 'price', 'detail', 'nameRestaurantFood', 'imgFood',
                  'createBy', 'createAt', 'quantityPurchased', 'typeFoodEntityId',
                  'restaurantEntityId', 'status', 'distance', 'nameType']

    def get_quantityPurchased(self, obj):
        return obj.quantity_purchased if obj.quantity_purchased is not None else ''



class RestaurantSerializer(serializers.ModelSerializer):
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
