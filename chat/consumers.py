import json
from asgiref.sync import async_to_sync
from chat.serializers import MessageSerializer
from chat.models import Message, ChatRoom
from channels.generic.websocket import WebsocketConsumer
from rest_framework.renderers import JSONRenderer
from django.contrib.auth.models import User


class ChatConsumer(WebsocketConsumer):
    """
    WebsocketConsumer is written as Synchronous, but we have
    used channel_layers in the functions, which are Asynchronous.
    So we have to convert them to Synchronous.
    """

    def new_message(self, data):
        content = data['message']
        username = data['username']
        room_name = data['room_name']
        chat = ChatRoom.objects.get(room_name=room_name)
        author = User.objects.get(username=username)
        message = Message.objects.create(content=content, author=author, chat=chat)
        result = eval(self.message_serializer(message))
        self.send_message(result)

    def fetch_message(self, data):
        room_name = data['room_name']
        query_set = Message.room_message(self, room_name)
        message = self.message_serializer(query_set)  # convert QuerySet to Json
        content = {
            'message': eval(message),  # eval returns bytestring to json
            'command': 'fetch_message'
        }
        self.chat_message(content)  # call chat_message and forward content to it

    def send_image(self, data):
        content = data['content']
        username = data['__str__']
        room_name = data['room_name']
        chat = ChatRoom.objects.get(room_name=room_name)
        author = User.objects.get(username=username)
        message = Message.objects.create(content=content, author=author, chat=chat)
        self.send_message(data)

    def message_serializer(self, query):
        serializer = MessageSerializer(query,
                                       many=(lambda query: True if (query.__class__.__name__ == 'QuerySet') else False)(
                                           query))
        content = JSONRenderer().render(serializer.data)
        return content

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group (Channel Layers)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name,
        )

        self.accept()

    commands = {
        'new_message': new_message,
        'fetch_message': fetch_message,
        'send_image': send_image
    }

    def disconnect(self, code):
        # Leave room group (Channel Layers)
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name,
        )

    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        text_to_dict = json.loads(text_data)

        command = text_to_dict['command']

        self.commands[command](self, text_to_dict)

    def send_message(self, message):
        command = message.get('command', None)
        # Send message to room group  -->  Create an event and send to 'chat_message' function
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "content": message['content'],
                "command": (lambda command: "send_image" if (command == 'send_image') else "new_message")(command),
                "__str__": message['__str__']
            }  # Dict is an event with 'message' key!
        )

    # Receive message from room group
    def chat_message(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps(event))
