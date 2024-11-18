# myapp/consumers.py

import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Message,Conversation
from django.contrib.auth.models import User
from django.utils.timezone import localtime  # To handle timezone-aware datetime objects

class MyConsumer(WebsocketConsumer):
    def connect(self):
        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.room_group_name = "chat_%s" % self.conversation_id
        
        self.user = self.scope['user']
        try:
            self.conversation = Conversation.objects.get(id=self.conversation_id)
        except Conversation.DoesNotExist:
            self.send(text_data=json.dumps({"error": 'Conversation Not Found'}))
            return self.close()
       
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        print("disconnect",close_code)
        pass
    

    # # # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        message = text_data_json["message"]
        # Get the receiver using the conversation's get_receiver method
        receiver = self.conversation.get_receiver(self.user)
        message_obj = Message.objects.create(conversation=self.conversation,sender=self.user,receiver=receiver,text=message)
        # Send message to room group
        # Convert timestamp to a string (ISO format or custom format)
        formatted_timestamp = localtime(message_obj.timestamp).strftime('%Y-%m-%d %H:%M:%S')
        
        # Send the message and timestamp to the room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                "type": "chat_message",
                "message": message_obj.text,
                "user_id": self.user.id,
                'sender':self.user.id,
                'sender_username':self.user.username,
                'receiver':receiver.id,
                "timestamp": formatted_timestamp  # Send as a string
            }
        )

    # # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        timestamp = event["timestamp"]
        
        print('event',event)
        # Send message to WebSocket
        receiver = self.conversation.get_receiver(self.user)
        
        self.send(text_data=json.dumps({"event": event}))
