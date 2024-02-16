# myapp/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import BillDetailEntity, BillEntity
from ProductManager.models import FoodEntity
from channels.db import database_sync_to_async
from AccountEntity.models import AccountEntity
class CheckoutConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user_id = self.scope.get('user_id')
        self.room_group_name = "bills"

        if user_id:
            print(f"Authenticated user: {user_id}")
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            print("Unauthenticated user")
            await self.close()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    @database_sync_to_async
    def add_bill_to_db(self, data):
        user_id = self.scope.get('user_id')
        user = AccountEntity.objects.get(id=user_id)
        bill_data = {
            'ship_fee': data.get("shipFee", 0),
            'total_amount': data.get("totalAmount", 0),
            'finish_time': data.get("finishTime", ''),
            'note': data.get("note", ''),
            'code': data.get("codeVoucher", ''),
            'account_entity': user,
            'create_by': user,
            'modified_by': user,
        }
        bill = BillEntity.objects.create(**bill_data)

        for bill_food_request_data in data.get("billFoodRequests", []):
            food = FoodEntity.objects.get(id=bill_food_request_data['foodId'])
            # food.update_quantity_purchased(
            #     data.get('orderStatus', None), bill_food_request_data['quantity'])

            # food.update_restaurant_quantity_sold(food)
            BillDetailEntity.objects.create(
                bill_entity_id=bill,
                food_entity_id=food,
                quantity=bill_food_request_data['quantity']
            )
        return bill

    async def receive(self, text_data):
        data = json.loads(text_data)
        try:
            bill = await self.add_bill_to_db(data)
            print(bill)
            await self.channel_layer.group_send(self.room_group_name,{
                'type': 'created_bill',
                'bill_id': bill.id,
                'message': 'Bill created successfully.',
            })
        except Exception as e:
            await self.send({
                'type': 'error',
                'message': f'Error occurred: {str(e)}'
            })

    async def created_bill(self, event):
     
        await self.send(text_data=json.dumps(event))