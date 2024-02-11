# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("notifications_pph", self.channel_name)

    async def disconnect(self, close_code):
        pass

    async def send_notification(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))

    async def send_data_extraction_notification(self, message):
        await self.send_notification({'message': message})


