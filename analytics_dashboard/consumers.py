import json
from channels.generic.websocket import AsyncWebsocketConsumer

class RealtimeMonitoringConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("monitoring", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("monitoring", self.channel_name)

    async def receive_json(self, content, **kwargs):
        if content.get('action') == 'ping':
            await self.send_json({'event': 'pong'})

    async def sensor_update(self, event):
        await self.send_json({
            'event': 'sensor_update',
            'payload': event['data'],
        })

    async def alert_update(self, event):
        await self.send_json({
            'event': 'alert_update',
            'payload': event['data'],
        })

    async def status_update(self, event):
        await self.send_json({
            'event': 'status_update',
            'payload': event['data'],
        })
