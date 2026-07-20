import { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";
import type { Message } from "@entities/message";
import { sendTextMessage } from "../api/sendTextMessage";

interface UseSendTextMessageOptions {
  sessionId: string | null;
  onMessage: (messages: Message[]) => void;
  onEnded: () => void;
}

interface UseSendTextMessageResult {
  send: (text: string) => Promise<void>;
  isLoading: boolean;
  error: string | null;
}

function createMessage(role: Message["role"], content: string): Message {
  return {
    id: crypto.randomUUID(),
    role,
    content,
  };
}

export function useSendTextMessage({
  sessionId,
  onMessage,
  onEnded,
}: UseSendTextMessageOptions): UseSendTextMessageResult {
  const { t } = useTranslation();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const send = useCallback(
    async (text: string) => {
      if (!sessionId || !text.trim()) return;

      setIsLoading(true);
      setError(null);

      const userMessage = createMessage("user", text.trim());
      onMessage([userMessage]);

      try {
        const response = await sendTextMessage(text.trim(), sessionId);
        const assistantMessage = createMessage("assistant", response.response);
        onMessage([assistantMessage]);

        if (response.ended) {
          onEnded();
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : t("chat.sendError"));
      } finally {
        setIsLoading(false);
      }
    },
    [sessionId, onMessage, onEnded, t],
  );

  return { send, isLoading, error };
}
