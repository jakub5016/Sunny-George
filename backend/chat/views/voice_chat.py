import asyncio
import uuid

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from chat.locale_content import LocaleContentProvider
from chat.services import ChatSessionService, VoiceChatService

class VoiceChatView(APIView):
    def post(self, request):
        audio = request.FILES.get("audio")
        if not audio:
            return Response(
                {"detail": "An audio file is required (field 'audio')."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        session_id = str(request.data.get("session_id") or uuid.uuid4())
        locale_provider = LocaleContentProvider()
        locale = locale_provider.normalize(request.data.get("locale"))

        if request.data.get("start", "false").lower() in ("true", "1"):
            asyncio.run(ChatSessionService(locale_provider).start(session_id, locale))

        result = asyncio.run(
            VoiceChatService(session_id, locale, locale_provider).process(audio)
        )
        return Response(result)
