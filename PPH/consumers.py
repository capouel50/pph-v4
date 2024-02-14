# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("notifications_pph", self.channel_name)
        # Envoyez un message de test directement après la connexion
        await self.send(text_data=json.dumps(
            {"notification": {"message": "Demande prise en compte", "notification_type": "success"}}))

    async def disconnect(self, close_code):
        pass

    async def send_notification(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))

    async def send_data_extraction_notification(self, event):
        print("Consumer")
        # Extraction de l'objet notification de l'événement
        notification = event['notification']
        # Envoi de l'objet notification comme JSON au client
        await self.send(text_data=json.dumps({
            'notification': notification
        }))


