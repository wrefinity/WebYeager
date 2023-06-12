import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging
from django.template.loader import get_template

logger = logging.getLogger(__name__)
'''
FastAPI connect
'''
class FastAPIConsumer(AsyncWebsocketConsumer):
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
        logger.info('===Received message=====')

        try:
            if 'nearby_entities' in data:
                template_name = "partials/Events/agent_event.html"
                html = get_template(template_name).render(context={"data": data})
                
                await self.send(text_data=html)
            else:
                template_name = "partials/Events/event.html"
            
                html = get_template(template_name).render(context={"data": data})
                await self.send(text_data=html)
        except Exception as e:
            print("An error occurred while sending the data:", e)

