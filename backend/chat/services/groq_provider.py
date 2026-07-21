from groq import Groq
from langchain_groq import ChatGroq


class GroqProvider:
    _instance: "GroqProvider | None" = None
    _client: Groq | None = None

    def __new__(cls) -> "GroqProvider":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def client(self) -> Groq:
        if self._client is None:
            GroqProvider._client = Groq()
        return GroqProvider._client

    def create_chat_model(self, model: str = "openai/gpt-oss-20b") -> ChatGroq:
        return ChatGroq(model=model)
