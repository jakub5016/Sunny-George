from django.urls import path

from chat.views.text_chat import TextChatView
from chat.views.voice_chat import VoiceChatView

urlpatterns = [
    path("chat/text/", TextChatView.as_view(), name="chat-text"),
    path("chat/voice/", VoiceChatView.as_view(), name="chat-voice"),
]
