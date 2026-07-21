import { useCallback, useState } from "react";
import type { Message } from "@entities/message";
import { startChat } from "../api/startChat";

interface UseStartChatResult {
  sessionId: string | null;
  messages: Message[];
  isLoading: boolean;
  error: string | null;
  start: () => Promise<void>;
}

function createMessage(role: Message["role"], content: string): Message {
  return {
    id: crypto.randomUUID(),
    role,
    content,
  };
}

export function useStartChat(): UseStartChatResult {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const start = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await startChat(sessionId ?? undefined);
      setSessionId(response.session_id);
      setMessages([createMessage("assistant", response.response)]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to start conversation");
    } finally {
      setIsLoading(false);
    }
  }, [sessionId]);

  return { sessionId, messages, isLoading, error, start };
}
