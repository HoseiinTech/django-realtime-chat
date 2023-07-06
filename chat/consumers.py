import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    """
    WebsocketConsumer is written as Synchronous, but we have
    used channel_layers in the functions, which are Asynchronous.
    So we have to convert them to Synchronous.
    """

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group (Channel Layers)
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name,
        )

        await self.accept()

    async def disconnect(self, code):
        # Leave room group (Channel Layers)
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name,
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        text_to_dict = json.loads(text_data)
        message = text_to_dict['message']

        # Send message to room group  -->  Create an event and send to 'chat_message' function
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}  # Dict is an event with 'message' key!
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
