from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("ws/notifications/", NotificationConsumer.as_asgi()),
        # Ajoutez d'autres routages WebSocket au besoin
    ]),
})
