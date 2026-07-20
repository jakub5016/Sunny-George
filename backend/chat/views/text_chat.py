import asyncio
import uuid

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from chat.serializers.text_chat_serializer import TextChatSerializer
from chat.services import ChatSessionService, TextChatService

class TextChatView(APIView):
    def post(self, request):
        serializer = TextChatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        session_id = str(data.get("session_id") or uuid.uuid4())

        locale = data.get("locale")

        if data.get("start"):
            result = asyncio.run(ChatSessionService().start(session_id, locale))
            return Response(result)

        message = data.get("message", "").strip()
        if not message:
            return Response(
                {"detail": "The 'message' field is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        result = asyncio.run(TextChatService(session_id, locale).process(message))
        return Response(result)

