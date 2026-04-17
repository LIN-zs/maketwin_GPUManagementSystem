# reservations/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class GPUUpdateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'gpu_updates'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        pass  # 可忽略前端发来的消息

    async def send_update(self, event):
        """当组内广播 send_update 类型消息时调用，推送给前端"""
        await self.send(text_data=json.dumps({
            'type': 'reservation_update',
            'data': event['data']
        }))