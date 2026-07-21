from django.core.cache import cache
from django.test import TestCase
from langchain.messages import AIMessage, HumanMessage

from chat.services.chat_session_service import ChatSessionService


class ChatSessionServiceTests(TestCase):
    def setUp(self) -> None:
        cache.clear()
        self.service = ChatSessionService()
        self.session_id = "test-session-123"

    def test_session_key_format(self) -> None:
        self.assertEqual(
            self.service._get_session_key(self.session_id),
            "chat_session:test-session-123",
        )

    def test_save_and_load_conversation(self) -> None:
        messages = [HumanMessage(content="hello")]
        self.service.save_conversation(self.session_id, messages)
        self.assertEqual(self.service.load_conversation(self.session_id), messages)

    def test_load_returns_empty_list_when_missing(self) -> None:
        self.assertEqual(self.service.load_conversation(self.session_id), [])

    def test_reset_removes_session(self) -> None:
        self.service.save_conversation(self.session_id, [AIMessage(content="hi")])
        self.service.reset(self.session_id)
        self.assertEqual(self.service.load_conversation(self.session_id), [])

    def test_start_resets_and_returns_greeting(self) -> None:
        import asyncio

        result = asyncio.run(self.service.start(self.session_id, "en"))

        self.assertEqual(result["session_id"], self.session_id)
        self.assertFalse(result["ended"])
        self.assertIsNone(result["transcript"])
        self.assertIn("response", result)
        conversation = self.service.load_conversation(self.session_id)
        self.assertEqual(len(conversation), 1)
        self.assertIsInstance(conversation[0], AIMessage)
