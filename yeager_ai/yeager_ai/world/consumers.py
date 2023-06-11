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
        
        
    # async def world_event(self, event):
    #     data = event['data']
    #     logger.info('===Received message=====')
    #     # html_message = f"<div hx-swap-oob='beforeend:#messages'>Welcome <p>{data['event_type']}</p></div>"
    #     # print(html_message)
    #     try:
    #         html = get_template("partials/notifier.html").render(
    #                 context={"data": data}
    #             )
    #         await self.send(text_data=html)
    #     except Exception as e:
    #         print("An error occurred while sending the data:", e)
            
    async def world_event(self, event):
        data = event['data']
        try:
            json_data = json.dumps({"eventData": data})  # Include event data with a specific key
            await self.send(text_data=json_data)  # Send JSON data through WebSocket
        except Exception as e:
            print("An error occurred while sending the data:", e)