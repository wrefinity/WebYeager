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
    
    async def add_to_grouped_events(self, new_data):
        sender_id = new_data.get('sender_id', None)
# Check if sender_id is available in new_data and the sender_id is a 
        # string type considering that other id exist with different data type
        if sender_id and isinstance(sender_id, str):
            sender_key = sender_id.lower()

            unique_event = {item['created_at'] for item in self.grouped_events[sender_key]}
            # Check if the created_at value is unique

            if new_data['created_at'] not in unique_event:
                
                # Check if the sender_key already exists in the grouped_events
                
                if sender_key in self.grouped_events.keys():
                    
                    # Second time event: Append child div (discussion) to the parent div (e.g., chamath)
                    template_name = "partials/Events/agent_body.html"
                    body_html = get_template(template_name).render(context={"group_data": new_data})
                    await self.send(text_data=f'<div id="body" hx-append>{body_html}</div>')
                else:
                    
                    # First time an agent event stream is coming: Display both the parent div (e.g., chamath) 
                    # and the discussion (as child) by appending the child to the parent
                    
                    #sending the grouped_events here so i can have accesss to the key i.e sender_key here
                    
                    template_name = "partials/Events/agent_event.html"
                    html = get_template(template_name).render(context={"grouped_items": self.grouped_events})
                    await self.send(text_data=html)
                    
                    # since it's the first time we also  need to add the body with the dta it comes with
        
                    template_body = "partials/Events/agent_body.html"
                    body_html = get_template(template_body).render(context={"group_data": new_data})
                    await self.send(text_data=f'<div id="body" hx-append>{body_html}</div>')
                    
                # Append the new_data to the grouped_events dictionary
                
                self.grouped_events[sender_key].append(new_data)

                print("================================")
                print(new_data)

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
