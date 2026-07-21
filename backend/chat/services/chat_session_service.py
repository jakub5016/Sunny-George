from django.core.cache import cache
from langchain.messages import AIMessage

from chat.locale_content import LocaleContentProvider


class ChatSessionService:
    SESSION_PREFIX = "chat_session:"
    SESSION_TTL = 3600

    def __init__(self, locale_provider: LocaleContentProvider | None = None) -> None:
        self._locale_provider = locale_provider or LocaleContentProvider()

    def _get_session_key(self, session_id: str) -> str:
        return f"{self.SESSION_PREFIX}{session_id}"

    def load_conversation(self, session_id: str) -> list:
        return cache.get(self._get_session_key(session_id), [])

    def save_conversation(self, session_id: str, conversation: list) -> None:
        cache.set(self._get_session_key(session_id), conversation, self.SESSION_TTL)

    def reset(self, session_id: str) -> None:
        cache.delete(self._get_session_key(session_id))

    async def start(self, session_id: str, locale: str | None = None) -> dict:
        start_text = self._locale_provider.get_content(locale).start_text
        self.reset(session_id)
        self.save_conversation(session_id, [AIMessage(content=start_text)])
        return {
            "response": start_text,
            "session_id": session_id,
            "ended": False,
            "transcript": None,
        }
