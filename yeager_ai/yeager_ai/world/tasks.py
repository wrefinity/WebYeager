import requests
from celery import shared_task
import asyncio
import json
import websockets
from channels.layers import get_channel_layer


async def fetch_data_from_api(websocket_url):
    # Connect to the external API WebSocket and retrieve data
    async with websockets.connect(websocket_url) as websocket:
        while True:
            data = await websocket.recv()
            channel_layer = get_channel_layer()
            channel_world = 'world'
            data = json.loads(data)
            print(data)
            # Prepare the event to be broadcasted
            event = {
                'type': 'world_event',
                'data': data,
            }
            
           
            try:
                if data:
                    await channel_layer.group_send(channel_world, event)
                  
                    # async_to_sync(channel_layer.group_send)(channel_world, event)
            except Exception as e:
                print(f'Error during broadcast: {str(e)}')

@shared_task
def run_socket_task(mocked_event_file, default_preview_urls):
    requests.post(default_preview_urls, json=mocked_event_file, headers={"Content-Type": "application/json"})
    



@shared_task
def get_data_from_api(socket_url):
    # Connect to the external API WebSocket and retrieve data
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch_data_from_api(socket_url))
