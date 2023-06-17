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
    async def add_to_grouped_events(self, new_data):
        sender_id = new_data.get('sender_id')

        # Check if sender_id is available in new_data
        if sender_id:
            sender_key = sender_id.lower()  # Convert the sender_id to lowercase

            unique_event = {item['created_at'] for item in self.grouped_events.get(sender_key, [])}

            if new_data['created_at'] not in unique_event:
                # Add the new_data to the grouped_events
                self.grouped_events.setdefault(sender_key, []).append(new_data)
                
                print("================================")
                print(self.grouped_events)
                
                # Render the updated event HTML template
                template_name = "partials/Events/agent_event.html"
                html = get_template(template_name).render(context={"grouped_events": self.grouped_events})
                
                # Send the updated event HTML to the client
                await self.send(text_data=html)
                
                # Render the body HTML template for the updated grouped_events
                template_name = "partials/Events/agent_body.html"
                body_html = get_template(template_name).render(context={"grouped_events": self.grouped_events})
                
                await self.send(text_data=f'<div id="body" hx-append>{body_html}</div>')



    async def add_to_single_events(self, new_data):
        if not any(item['created_at'] == new_data['created_at'] for item in self.single_events):
            self.single_events.append(new_data)
            template_name = "partials/Events/event.html"
            html = get_template(template_name).render(context={"data": new_data})
            await self.send(text_data=html)


    async def world_event(self, event):
        new_data = event['data']
        try:
            await self.add_to_grouped_events(new_data)

            await self.add_to_single_events(new_data)

        except Exception as e:
            logger.error("An error occurred: %s", e)
