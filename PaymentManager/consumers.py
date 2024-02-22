# myapp/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import BillDetailEntity, BillEntity
from ProductManager.models import FoodEntity
from channels.db import database_sync_to_async
from AccountEntity.models import AccountEntity,VoucherEntity
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
 
            BillDetailEntity.objects.create(
                bill_entity=bill,
                food_entity=food,
                quantity=bill_food_request_data['quantity']
            )
        if len(bill_data['code'])>0:
            voucher = VoucherEntity.objects.get(code=bill_data['code'])
            voucher.delete_one_quantity()
        return bill

    async def receive(self, text_data):
        data = json.loads(text_data)
        try:
            bill = await self.add_bill_to_db(data)
            await self.channel_layer.group_send(self.room_group_name,{
                'type': 'created_bill',
                'bill_id': bill.id,
                'send_by':bill.account_entity.username,
                'message': 'Bill created successfully.',
            })
        except Exception as e:
            await self.send({
                'type': 'error',
                'message': f'Error occurred: {str(e)}'
            })

    async def created_bill(self, event):
     
        await self.send(text_data=json.dumps(event))