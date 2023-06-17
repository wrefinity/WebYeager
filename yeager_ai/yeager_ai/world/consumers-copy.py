import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging
from django.template.loader import get_template
from collections import defaultdict

logger = logging.getLogger(__name__)
'''
FastAPI connect
'''
class FastAPIConsumer(AsyncWebsocketConsumer):
    
    grouped_events = defaultdict(list)
    single_events = []
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
    
    
    # sending to grouped agents
    async def add_data(self, sender_id, data):
        unique_event = set(item['created_at'] for item in self.grouped_events[sender_id])
        if data['created_at'] not in unique_event:
            self.grouped_events[sender_id].append(data) 
            template_name = "partials/Events/agent_event.html"
            html = get_template(template_name).render(context={"grouped_events": self.grouped_events})
            await self.send(text_data=html)
            
    # checking for duplicate within events list
    async def check_duplicate(self, new_dict):
        if len(self.single_events) == 0:
            return False
        for item in self.single_events:
            if item['created_at'] == new_dict['created_at']:
                return True
        return False
        
    async def world_event(self, event):
        
        new_data = event['data']
        try:
            if "sender_id" in new_data and not isinstance(new_data['sender_id'], list):
                sender_key = new_data['sender_id'].lower()
                await self.add_data(sender_key, new_data)
                
                
            # check event exitance before appending to the context data to be sent to the frontend 
            check_existance = await self.check_duplicate(new_data) 
            if not check_existance: # it does not exist append
                self.single_events.append(new_data)
                template_name = "partials/Events/event.html"
                html = get_template(template_name).render(context={"data": new_data})
                await self.send(text_data=html)  # Send data through WebSocket
                print("===================event=========================")
                print(self.single_events)
                print("===================event========================")
                
                
        except Exception as e:
            print("an error ", e)
        
        

    # async def world_event(self, event):
    #     data = event['data']
    #     try:
    #         if "sender_id" in data:
                
    #             data_key = str(data['sender_id']).lower()
    #             data_to_check = str(data['created_at'])
    #             print(type(self.grouped_events[data_key]))
    #             found = False
    #             if any(self.grouped_events.values()) and data_key in self.grouped_events:
    #                 found = any(item["created_at"] == data_to_check for item in self.grouped_events[data_key]) #check if the data alreay exits in the grouping
    #                 print("===================", found)
    #                 print(data['created_at'])
    #                 print("========more===========")

    #             if data_key in self.grouped_events and not isinstance(data_key, dict):
    #                 print("======runner more ========")
    #                 self.grouped_events[data_key].append(data)
    #             elif(not isinstance(data_key, dict)):
    #                 print("======runner first time ========")
    #                 self.grouped_events[data_key] = [data]


    #             # Send the data
    #             if not found and data.get("description", None):
    #                 template_name = "partials/Events/event.html"
    #                 html = get_template(template_name).render(context={"data": data})
    #                 await self.send(text_data=html)  # Send data through WebSocket
                    
    #             found = False
                
    #             template_name = "partials/Events/agent_event.html"
    #             html = get_template(template_name).render(context={"grouped_events": self.grouped_events})

    #             await self.send(text_data=html)


    #     except Exception as e:
    #         print("An error occurred while sending the data:", e)