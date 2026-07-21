import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from django.test import SimpleTestCase
from langchain.messages import AIMessage, HumanMessage

from chat.services.chat_agent_service import ChatAgentService
from chat.services.groq_provider import GroqProvider
from chat.services.text_chat_service import TextChatService
from chat.services.voice_chat_service import VoiceChatService


class GroqProviderTests(SimpleTestCase):
    def test_singleton_instance(self) -> None:
        self.assertIs(GroqProvider(), GroqProvider())

    @patch("chat.services.groq_provider.Groq")
    def test_client_lazy_initialization(self, mock_groq_cls: MagicMock) -> None:
        GroqProvider._client = None
        provider = GroqProvider()
        client = provider.client
        mock_groq_cls.assert_called_once()
        self.assertIs(client, mock_groq_cls.return_value)

    @patch("chat.services.groq_provider.ChatGroq")
    def test_create_chat_model(self, mock_chat_groq: MagicMock) -> None:
        model = GroqProvider().create_chat_model("test-model")
        mock_chat_groq.assert_called_once_with(model="test-model")
        self.assertEqual(model, mock_chat_groq.return_value)


class ChatAgentServiceTests(SimpleTestCase):
    @patch("chat.services.chat_agent_service.create_agent")
    @patch.object(ChatAgentService, "__init__", lambda self: None)
    def test_create_agent(self, mock_create_agent: MagicMock) -> None:
        service = ChatAgentService()
        service._groq = MagicMock()
        service._groq.create_chat_model.return_value = "model"
        service._system_prompt_provider = MagicMock()
        service._system_prompt_provider.get.return_value = "system prompt"

        agent = asyncio.run(service.create_agent("en"))

        service._system_prompt_provider.get.assert_called_once_with("en")
        mock_create_agent.assert_called_once_with(
            "model",
            [],
            system_prompt="system prompt",
        )
        self.assertEqual(agent, mock_create_agent.return_value)

    @patch.object(ChatAgentService, "__init__", lambda self: None)
    async def _run_agent_stream(self, events: list) -> tuple[str, list]:
        service = ChatAgentService()

        async def astream(*_args, **_kwargs):
            for event in events:
                yield event

        agent = MagicMock()
        agent.astream = astream
        conversation = [HumanMessage(content="hi")]
        return await service.run(agent, conversation)

    def test_run_collects_last_non_empty_ai_message(self) -> None:
        events = [
            {"messages": [AIMessage(content="  ")]},
            {"messages": [AIMessage(content="first")]},
            {"messages": [AIMessage(content="final reply")]},
        ]
        final_text, updated = asyncio.run(self._run_agent_stream(events))

        self.assertEqual(final_text, "final reply")
        self.assertEqual(len(updated), 3)
        self.assertEqual(updated[-1].content, "final reply")


class TextChatServiceTests(SimpleTestCase):
    @patch("chat.services.text_chat_service.ChatSessionService")
    @patch("chat.services.text_chat_service.ChatAgentService")
    def test_process_appends_message_and_returns_response(
        self,
        mock_agent_cls: MagicMock,
        mock_session_cls: MagicMock,
    ) -> None:
        session = mock_session_cls.return_value
        session.load_conversation.return_value = []
        agent = MagicMock()
        mock_agent_cls.return_value.create_agent = AsyncMock(return_value=agent)
        mock_agent_cls.return_value.run = AsyncMock(
            return_value=("assistant reply", [AIMessage(content="assistant reply")])
        )

        result = asyncio.run(TextChatService("sid-1", "pl").process("user question"))

        self.assertEqual(result["response"], "assistant reply")
        self.assertEqual(result["session_id"], "sid-1")
        self.assertFalse(result["ended"])
        session.save_conversation.assert_called_once()

    @patch("chat.services.text_chat_service.ChatSessionService")
    @patch("chat.services.text_chat_service.ChatAgentService")
    def test_process_marks_ended_for_end_message(
        self,
        mock_agent_cls: MagicMock,
        mock_session_cls: MagicMock,
    ) -> None:
        from chat.locale_content import LocaleContentProvider

        end_message = LocaleContentProvider().get_content("pl").end_message
        mock_session_cls.return_value.load_conversation.return_value = []
        mock_agent_cls.return_value.create_agent = AsyncMock(return_value=MagicMock())
        mock_agent_cls.return_value.run = AsyncMock(
            return_value=(end_message, [AIMessage(content=end_message)])
        )

        result = asyncio.run(TextChatService("sid-2", "pl").process("bye"))

        self.assertTrue(result["ended"])


class VoiceChatServiceTests(SimpleTestCase):
    @patch("chat.services.voice_chat_service.TextChatService")
    @patch.object(VoiceChatService, "transcribe", return_value="transcribed text")
    def test_process_attaches_transcript(
        self,
        _mock_transcribe: MagicMock,
        mock_text_chat_cls: MagicMock,
    ) -> None:
        mock_text_chat_cls.return_value.process = AsyncMock(
            return_value={
                "response": "reply",
                "session_id": "sid-v",
                "ended": False,
                "transcript": None,
            }
        )
        audio = MagicMock()

        result = asyncio.run(VoiceChatService("sid-v", "pl").process(audio))

        self.assertEqual(result["transcript"], "transcribed text")
        self.assertEqual(result["response"], "reply")

    @patch("chat.services.voice_chat_service.GroqProvider")
    def test_transcribe_calls_groq_whisper(self, mock_provider_cls: MagicMock) -> None:
        transcription = MagicMock()
        transcription.text = "  hello world  "
        mock_provider_cls.return_value.client.audio.transcriptions.create.return_value = transcription

        audio = MagicMock()
        audio.chunks.return_value = [b"audio-bytes"]

        text = VoiceChatService("sid", "en").transcribe(audio)

        self.assertEqual(text, "hello world")
        mock_provider_cls.return_value.client.audio.transcriptions.create.assert_called_once()
