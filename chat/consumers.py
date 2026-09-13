import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .services import ask_ai


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({
            "reason": "connection",
            "message": "Connected to server successfully"
        }))

    async def disconnect(self, code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data.get("message", "").strip()

        if not message:
            return

        await self.send(text_data=json.dumps({"reason":"start"}))
        try:
            async for chunk in ask_ai(message):
                await self.send(text_data=json.dumps({"reason":"chunk", "message":chunk}))
            await self.send(text_data=json.dumps({"reason": "end"}))
        except Exception as e:
            await self.send(text_data=json.dumps({
                "reason": "error",
                "message": f"Error: {str(e)}"
            }))
