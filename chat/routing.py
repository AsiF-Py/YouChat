from django.urls import path,re_path
from . import consumers
websocket_urlpatterns = [
re_path(r"ws/chat/(?P<conversation_id>[0-9a-f-]+)/$", consumers.MyConsumer.as_asgi()),
]