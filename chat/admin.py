from django.contrib import admin
from chat.models import Message, ChatRoom

admin.site.register(Message)
admin.site.register(ChatRoom)
