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
        
        if self.scope["user"].is_authenticated:
            # User is authenticated, proceed with connection
            self.channel_world = 'world'
            await self.channel_layer.group_add(self.channel_world, self.channel_name)
            await self.accept()
            logger.info('Connected to world channel')
            await self.send(text_data=json.dumps({
                'message': 'Connected'
            }))
        else:
            # User is not authenticated, close the connection
            await self.close()
       
        

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
            

            if "sender_id" in data:
                data_key = data['sender_id']
                # value = self.grouped_events.get(data_key, None)
                if data_key in self.grouped_events: # meaning sender id have already been added.
                    self.grouped_events[str(data_key).lower()].append(data)
                    print(self.grouped_events, "++already exist*****")
                    json_data = json.dumps({"groupedEvents": self.grouped_events})
                    await self.send(text_data=json_data)  # Send JSON data through WebSocket
                    
                else: # scenario where the sender_id is new instance
                    self.grouped_events[str(data_key).lower()] = [data]
                    print("=========checker=======", self.grouped_events)
                    json_data = json.dumps({"groupedEvents": self.grouped_events})
                    await self.send(text_data=json_data)  # Send JSON data through WebSocket
            else:
                json_data = json.dumps({"eventData": data}) 
                await self.send(text_data=json_data)  # Send JSON data through WebSocket
            

        except Exception as e:
            print("An error occurred while sending the data:", e)
            
            
# 1. check for sender id availability 
# created a dictionary of list
# if the current sender id is the first instance create an array for the sender id 
# else append it to its predecessors
# Note dictionary key should be sender id so as to enable subsequent check if instance availability 