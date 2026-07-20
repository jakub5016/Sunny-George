from io import BytesIO
from unittest.mock import AsyncMock, MagicMock, patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TextChatViewTests(APITestCase):
    @patch("chat.views.text_chat.ChatSessionService")
    def test_start_returns_greeting(self, mock_session_cls: MagicMock) -> None:
        mock_session_cls.return_value.start = AsyncMock(
            return_value={
                "response": "Hello",
                "session_id": "abc",
                "ended": False,
                "transcript": None,
            }
        )

        response = self.client.post(
            reverse("chat-text"),
            {"start": True, "locale": "en"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["response"], "Hello")

    def test_missing_message_returns_400(self) -> None:
        response = self.client.post(reverse("chat-text"), {"session_id": "abc"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("chat.views.text_chat.TextChatService")
    def test_message_returns_agent_reply(self, mock_service_cls: MagicMock) -> None:
        mock_service_cls.return_value.process = AsyncMock(
            return_value={
                "response": "Solar panels are great",
                "session_id": "abc",
                "ended": False,
                "transcript": None,
            }
        )

        response = self.client.post(
            reverse("chat-text"),
            {
                "message": "Tell me about panels",
                "session_id": "12345678-1234-5678-1234-567812345678",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["response"], "Solar panels are great")


class VoiceChatViewTests(APITestCase):
    def test_missing_audio_returns_400(self) -> None:
        response = self.client.post(reverse("chat-voice"), {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("chat.views.voice_chat.VoiceChatService")
    @patch("chat.views.voice_chat.ChatSessionService")
    def test_voice_message_returns_transcript(
        self,
        mock_session_cls: MagicMock,
        mock_voice_cls: MagicMock,
    ) -> None:
        mock_voice_cls.return_value.process = AsyncMock(
            return_value={
                "response": "reply",
                "session_id": "voice-1",
                "ended": False,
                "transcript": "user said hello",
            }
        )

        audio = BytesIO(b"fake-audio")
        audio.name = "test.wav"
        response = self.client.post(
            reverse("chat-voice"),
            {
                "audio": audio,
                "session_id": "12345678-1234-5678-1234-567812345678",
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["transcript"], "user said hello")
        mock_session_cls.return_value.start.assert_not_called()

    @patch("chat.views.voice_chat.VoiceChatService")
    @patch("chat.views.voice_chat.ChatSessionService")
    def test_voice_start_flag_triggers_session_start(
        self,
        mock_session_cls: MagicMock,
        mock_voice_cls: MagicMock,
    ) -> None:
        mock_session_cls.return_value.start = AsyncMock()
        mock_voice_cls.return_value.process = AsyncMock(
            return_value={
                "response": "reply",
                "session_id": "voice-2",
                "ended": False,
                "transcript": "hi",
            }
        )

        audio = BytesIO(b"fake-audio")
        audio.name = "test.wav"
        response = self.client.post(
            reverse("chat-voice"),
            {
                "audio": audio,
                "session_id": "22345678-1234-5678-1234-567812345678",
                "start": "true",
                "locale": "pl",
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_session_cls.return_value.start.assert_called_once()
