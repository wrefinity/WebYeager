from django.urls import path
from yeager_ai.world import consumers

websocket_urlpatterns = [
    path('ws/world/', consumers.FastAPIConsumer.as_asgi()),
]