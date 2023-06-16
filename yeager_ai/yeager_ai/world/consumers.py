import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging
from django.template.loader import get_template

logger = logging.getLogger(__name__)
'''
FastAPI connect
'''
class FastAPIConsumer(AsyncWebsocketConsumer):
    
    grouped_events = {}
    
    async def connect(self):
        self.channel_world = 'world'
        await self.channel_layer.group_add(self.channel_world, self.channel_name)
        await self.accept()
        logger.info('Connected to world channel')
        await self.send(text_data=json.dumps({
            'message': 'Connected'
        }))
        

    async def disconnect(self):
        await self.channel_layer.group_discard(
            self.channel_world, self.channel_name
        )
        logger.info('Disconnected from world channel')
        

    async def receive(self, text_data):
        logger.info('===Received message=====')
        
        
        

    async def world_event(self, event):
        data = event['data']
        try:
            if "sender_id" in data:
                data_key = data['sender_id']
                if data_key in self.grouped_events:
                    self.grouped_events[str(data_key).lower()].append(data)
                    json_data = json.dumps({"groupedEvents": self.grouped_events})
                    # print("===================")
                    
                    # print(self.grouped_events)
                    
                    # print("========more===========")
                    
                    await self.send(text_data=json_data)  # Send JSON data through WebSocket
                else:
                    self.grouped_events[str(data_key).lower()] = [data]

            template_name = "partials/Events/agent_event.html"
            html = get_template(template_name).render(context={"grouped_events": self.grouped_events})

            await self.send(text_data=html)

            # Send the data without filtering
            template_name = "partials/Events/event.html"
            html = get_template(template_name).render(context={"data": data})
            await self.send(text_data=html)  # Send JSON data through WebSocket

        except Exception as e:
            print("An error occurred while sending the data:", e)

