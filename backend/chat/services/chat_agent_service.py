from langchain.agents import create_agent
from langchain.messages import AIMessage

from chat.prompts import SystemPromptProvider

from .groq_provider import GroqProvider


class ChatAgentService:
    def __init__(self) -> None:
        self._groq = GroqProvider()
        self._system_prompt_provider = SystemPromptProvider()

    async def create_agent(self, locale: str | None = None):
        model = self._groq.create_chat_model()
        tools = []
        return create_agent(
            model,
            tools,
            system_prompt=self._system_prompt_provider.get(locale),
        )

    async def run(self, agent, conversation: list) -> tuple[str, list]:
        final_text = ""
        updated_conversation = list(conversation)

        async for event in agent.astream(
            {"messages": conversation},
            stream_mode="values",
        ):
            msg = event["messages"][-1]
            if isinstance(msg, AIMessage):
                text = msg.content.strip()
                if not text:
                    continue
                final_text = text
                updated_conversation.append(AIMessage(content=text))

        return final_text, updated_conversation
