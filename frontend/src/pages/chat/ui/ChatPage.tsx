import { useCallback, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import type { Message } from "@entities/message";
import { useSendTextMessage } from "@features/send-text-message";
import { startChat } from "@features/start-chat/api/startChat";
import { i18n, useLocale } from "@shared/lib/i18n";
import { ErrorBanner } from "@shared/ui/error-banner";
import { LoadingState } from "@shared/ui/loading-state";
import { ChatInterface } from "@widgets/chat-interface";
import styles from "./ChatPage.module.css";

export function ChatPage() {
  const { t } = useTranslation();
  const { locale } = useLocale();
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [chatEnded, setChatEnded] = useState(false);
  const [initError, setInitError] = useState<string | null>(null);
  const [isInitializing, setIsInitializing] = useState(true);

  const appendMessages = useCallback((newMessages: Message[]) => {
    setMessages((prev) => [...prev, ...newMessages]);
  }, []);

  const handleEnded = useCallback(() => {
    setChatEnded(true);
  }, []);

  const { send, isLoading: isSending, error: sendError } = useSendTextMessage({
    sessionId,
    onMessage: appendMessages,
    onEnded: handleEnded,
  });

  useEffect(() => {
    setIsInitializing(true);
    setChatEnded(false);
    setInitError(null);

    startChat()
      .then((response) => {
        setSessionId(response.session_id);
        setMessages([
          {
            id: crypto.randomUUID(),
            role: "assistant",
            content: response.response,
          },
        ]);
      })
      .catch((err) =>
        setInitError(
          err instanceof Error ? err.message : i18n.t("chat.initError"),
        ),
      )
      .finally(() => setIsInitializing(false));
  }, [locale]);

  const disabled = chatEnded || isSending || isInitializing;

  if (isInitializing) {
    return (
      <div className={styles.page}>
        <LoadingState message={t("common.loading")} />
      </div>
    );
  }

  const error = initError ?? sendError;

  return (
    <div className={styles.page}>
      <main className={styles.content}>
        {error && <ErrorBanner message={error} />}

        <ChatInterface
          messages={messages}
          sessionId={sessionId}
          disabled={disabled}
          onTextSubmit={send}
          onMessage={appendMessages}
          onEnded={handleEnded}
        />

        {chatEnded && (
          <p className={`${styles.statusBanner} ${styles.endedBanner}`}>
            {t("chat.endedBanner")}
          </p>
        )}
      </main>
    </div>
  );
}
