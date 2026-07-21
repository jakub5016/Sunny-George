from langchain.messages import AIMessage, HumanMessage

from chat.locale_content import LocaleContentProvider
from config.const import MAX_MESSAGES

from .chat_agent_service import ChatAgentService
from .chat_session_service import ChatSessionService


class TextChatService:
    def __init__(
        self,
        session_id: str,
        locale: str | None = None,
        locale_provider: LocaleContentProvider | None = None,
    ) -> None:
        self._session_id = session_id
        self._locale_provider = locale_provider or LocaleContentProvider()
        self._locale = self._locale_provider.normalize(locale)
        self._content = self._locale_provider.get_content(self._locale)
        self._session = ChatSessionService(locale_provider=self._locale_provider)
        self._agent = ChatAgentService()

    async def process(self, message: str) -> dict:
        agent = await self._agent.create_agent(self._locale)
        conversation = self._session.load_conversation(self._session_id)

        if not conversation:
            conversation = [AIMessage(content=self._content.start_text)]

        conversation.append(HumanMessage(content=message))
        conversation = conversation[-MAX_MESSAGES:]

        response_text, conversation = await self._agent.run(agent, conversation)
        self._session.save_conversation(self._session_id, conversation)

        return {
            "response": response_text,
            "session_id": self._session_id,
            "ended": response_text in self._content.end_messages,
            "transcript": None,
        }
