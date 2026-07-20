from django.test import SimpleTestCase

from chat.locale_content import (
    DEFAULT_LOCALE,
    ChatLocaleContent,
    LocaleContentProvider,
)
from chat.prompts import SystemPromptProvider


class LocaleContentProviderTests(SimpleTestCase):
    def setUp(self) -> None:
        self.provider = LocaleContentProvider()

    def test_normalize_supported(self) -> None:
        self.assertEqual(self.provider.normalize("pl"), "pl")
        self.assertEqual(self.provider.normalize("en"), "en")

    def test_normalize_fallback(self) -> None:
        self.assertEqual(self.provider.normalize(None), DEFAULT_LOCALE)
        self.assertEqual(self.provider.normalize("de"), DEFAULT_LOCALE)

    def test_get_content_pl_and_en(self) -> None:
        pl = self.provider.get_content("pl")
        en = self.provider.get_content("en")

        self.assertIsInstance(pl, ChatLocaleContent)
        self.assertNotEqual(pl.start_text, en.start_text)

    def test_end_messages_property(self) -> None:
        content = self.provider.get_content("pl")
        self.assertEqual(len(content.end_messages), 2)
        self.assertIn(content.end_message, content.end_messages)


class SystemPromptProviderTests(SimpleTestCase):
    def setUp(self) -> None:
        self.locale_provider = LocaleContentProvider()
        self.provider = SystemPromptProvider(self.locale_provider)

    def test_get_returns_locale_specific_text(self) -> None:
        self.assertEqual(
            self.provider.get("en"),
            self.locale_provider.get_content("en").system_prompt,
        )
        self.assertEqual(
            self.provider.get(None),
            self.locale_provider.get_content(DEFAULT_LOCALE).system_prompt,
        )

    def test_get_default(self) -> None:
        self.assertEqual(
            self.provider.get_default(),
            self.locale_provider.get_content(DEFAULT_LOCALE).system_prompt,
        )
