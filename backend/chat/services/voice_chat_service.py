import tempfile

from asgiref.sync import sync_to_async

from chat.locale_content import LocaleContentProvider

from .groq_provider import GroqProvider
from .text_chat_service import TextChatService


class VoiceChatService:
    def __init__(
        self,
        session_id: str,
        locale: str | None = None,
        locale_provider: LocaleContentProvider | None = None,
    ) -> None:
        self._session_id = session_id
        self._locale_provider = locale_provider or LocaleContentProvider()
        self._locale = self._locale_provider.normalize(locale)

    def transcribe(self, audio_file) -> str:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            for chunk in audio_file.chunks():
                tmp.write(chunk)
            tmp_path = tmp.name

        with open(tmp_path, "rb") as file:
            transcription = GroqProvider().client.audio.transcriptions.create(
                file=(tmp_path, file.read()),
                model="whisper-large-v3-turbo",
                language=self._locale,
                temperature=0,
                response_format="verbose_json",
            )

        return transcription.text.strip()

    async def process(self, audio_file) -> dict:
        transcript = await sync_to_async(self.transcribe)(audio_file)
        result = await TextChatService(
            self._session_id,
            self._locale,
            locale_provider=self._locale_provider,
        ).process(transcript)
        result["transcript"] = transcript
        return result
