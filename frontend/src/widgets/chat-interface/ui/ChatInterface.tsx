import { useTranslation } from "react-i18next";
import type { Message } from "@entities/message";
import { TextMessageForm } from "@features/send-text-message";
import { VoiceRecorder } from "@features/send-voice-message";
import { ChatWindow } from "@widgets/chat-window";
import styles from "./ChatInterface.module.css";

interface ChatInterfaceProps {
  messages: Message[];
  disabled?: boolean;
  sessionId: string | null;
  displayLabel?: string;
  textLabel?: string;
  placeholder?: string;
  showVoice?: boolean;
  voiceLabel?: string;
  onTextSubmit: (text: string) => void;
  onMessage: (messages: Message[]) => void;
  onEnded: () => void;
}

export function ChatInterface({
  messages,
  disabled = false,
  sessionId,
  displayLabel,
  textLabel,
  placeholder,
  showVoice = true,
  voiceLabel,
  onTextSubmit,
  onMessage,
  onEnded,
}: ChatInterfaceProps) {
  const { t } = useTranslation();
  const resolvedDisplayLabel = displayLabel ?? t("chat.conversation");
  const resolvedTextLabel = textLabel ?? t("chat.messageLabel");
  const resolvedPlaceholder = placeholder ?? t("chat.placeholder");
  const resolvedVoiceLabel = voiceLabel ?? t("chat.recordVoice");

  return (
    <section className={styles.chat} aria-label={resolvedDisplayLabel}>
      <ChatWindow
        messages={messages}
        label={resolvedDisplayLabel}
        variant="embedded"
        compact
      />

      <footer className={styles.composer}>
        <TextMessageForm
          label={resolvedTextLabel}
          placeholder={resolvedPlaceholder}
          disabled={disabled}
          variant="composer"
          onSubmit={onTextSubmit}
        />
        {showVoice && (
          <VoiceRecorder
            label={resolvedVoiceLabel}
            sessionId={sessionId}
            disabled={disabled}
            variant="inline"
            onMessage={onMessage}
            onEnded={onEnded}
          />
        )}
      </footer>
    </section>
  );
}
