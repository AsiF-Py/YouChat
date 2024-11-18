from django.contrib import admin
from .models import Message,Conversation
# Register your models here.


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ["id",]
admin.site.register(Message)
# admin.site.register(Conversation)

