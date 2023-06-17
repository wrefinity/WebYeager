import json
import logging
from collections import defaultdict
from django.template.loader import get_template
from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)

class FastAPIConsumer(AsyncWebsocketConsumer):
    grouped_events = dict()
    single_events = []

    async def connect(self):
        self.channel_world = 'world'
        await self.channel_layer.group_add(self.channel_world, self.channel_name)
        await self.accept()
        logger.info('Connected to world channel')
        await self.send(text_data=json.dumps({'message': 'Connected'}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.channel_world, self.channel_name)
        logger.info('Disconnected from world channel')

    async def receive(self, text_data):
        logger.info('Received message: %s', text_data)

    async def world_event(self, event):
        new_data = event['data']
        try:
            if isinstance(new_data.get('sender_id'), str):
                sender_key = new_data['sender_id'].lower()

                unique_event = {item['created_at'] for item in self.grouped_events.get(sender_key, [])}
                if new_data['created_at'] not in unique_event:
                    self.grouped_events.setdefault(sender_key, []).append(new_data)
                    template_name = "partials/Events/agent_event.html"
                    html = get_template(template_name).render(context={"grouped_events": self.grouped_events})
                    await self.send(text_data=html)
            if not any(item['created_at'] == new_data['created_at'] for item in self.single_events):
                self.single_events.append(new_data)
                template_name = "partials/Events/event.html"
                html = get_template(template_name).render(context={"data": new_data})
                await self.send(text_data=html)

        except Exception as e:
            logger.error("An error occurred: %s", e)
