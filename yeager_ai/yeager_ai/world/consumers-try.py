import json
import logging
from collections import defaultdict
from django.template.loader import get_template
from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)

class FastAPIConsumer(AsyncWebsocketConsumer):
    grouped_events = defaultdict(list)
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

                unique_event = {item['created_at'] for item in self.grouped_events[sender_key]}
                if new_data['created_at'] not in unique_event:
                    self.grouped_events[sender_key].append(new_data)

                    # Retrieve additional details
                    event_type = new_data['event_type']
                    sender_id = new_data['sender_id']
                    message = new_data['message']
                    description = new_data['description']
                    created_at = new_data['created_at']
                    target_id = new_data['target_id']
                    nearby_entities = new_data['nearby_entities']
                    nearby_entities_name = nearby_entities.get('name')
                    nearby_entities_created_at = nearby_entities.get('created_at')

                    # Convert defaultdict to a regular dictionary
                    grouped_events_dict = dict(self.grouped_events)

                    template_name = "partials/Events/agent_event.html"
                    html = get_template(template_name).render(context={
                        "grouped_events": grouped_events_dict,
                        "event_type": event_type,
                        "sender_id": sender_id,
                        "message": message,
                        "description": description,
                        "created_at": created_at,
                        "target_id": target_id,
                        "nearby_entities_name": nearby_entities_name,
                        "nearby_entities_created_at": nearby_entities_created_at
                    })
                    await self.send(text_data=html)

            if not any(item['created_at'] == new_data['created_at'] for item in self.single_events):
                self.single_events.append(new_data)

                # Retrieve additional details
                event_type = new_data['event_type']
                sender_id = new_data['sender_id']
                message = new_data['message']
                description = new_data['description']
                created_at = new_data['created_at']
                target_id = new_data['target_id']
                nearby_entities = new_data['nearby_entities']
                nearby_entities_name = nearby_entities.get('name')
                nearby_entities_created_at = nearby_entities.get('created_at')

                template_name = "partials/Events/event.html"
                html = get_template(template_name).render(context={
                    "data": new_data,
                    "event_type": event_type,
                    "sender_id": sender_id,
                    "message": message,
                    "description": description,
                    "created_at": created_at,
                    "target_id": target_id,
                    "nearby_entities_name": nearby_entities_name,
                    "nearby_entities_created_at": nearby_entities_created_at
                })
                await self.send(text_data=html)

        except Exception as e:
            logger.error("An error occurred: %s", e)
