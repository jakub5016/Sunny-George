from chat.locale_content import DEFAULT_LOCALE, LocaleContentProvider


class SystemPromptProvider:
    def __init__(self, locale_provider: LocaleContentProvider | None = None) -> None:
        self._locale_provider = locale_provider or LocaleContentProvider()

    def get(self, locale: str | None) -> str:
        return self._locale_provider.get_content(locale).system_prompt

    def get_default(self) -> str:
        return self.get(DEFAULT_LOCALE)
