from django.db import models
from django.contrib.auth.models import User


class ChatRoom(models.Model):
    room_name = models.CharField(max_length=350)
    member = models.ManyToManyField(User, related_name='chat_room', null=True, blank=True)

    def __str__(self):
        return self.room_name


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    chat = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, blank=True)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def room_message(self, room_name):
        return Message.objects.filter(chat__room_name=room_name).order_by('-time_stamp')

    def __str__(self) -> str:
        return self.author.username
