from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Message,Conversation
from django.db.models import Q
# Create your views here.
def index(request,conversation_id):
    user = request.user
    conversation = Conversation.objects.get(id=conversation_id)
    receiver = conversation.get_receiver(user)
    
    # Fetch messages between the user and the friend
    messages = Message.objects.filter(
        (Q(sender=user) & Q(receiver=receiver)) | 
        (Q(sender=receiver) & Q(receiver=user))
    ).order_by('timestamp')
    
    
    context = {
        'messages': messages,
        'friend': receiver,
        'conversation_id': conversation_id,
        
    }
    return render(request,"chat.html",context)