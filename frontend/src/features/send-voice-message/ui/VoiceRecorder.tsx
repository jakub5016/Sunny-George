import { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";
import type { Message } from "@entities/message";
import { sendVoiceMessage } from "../api/sendVoiceMessage";
import { useVoiceRecorder } from "../model/useVoiceRecorder";
import styles from "./VoiceRecorder.module.css";

interface VoiceRecorderProps {
  sessionId: string | null;
  label?: string;
  disabled?: boolean;
  variant?: "default" | "inline";
  onMessage: (messages: Message[]) => void;
  onEnded: () => void;
}

function createMessage(
  role: Message["role"],
  content: string,
  transcript?: string,
): Message {
  return {
    id: crypto.randomUUID(),
    role,
    content,
    transcript,
  };
}

function MicrophoneIcon() {
  return (
    <svg
      width="22"
      height="22"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <path d="M12 2a3 3 0 0 0-3 3v6a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z" />
      <path d="M19 10v1a7 7 0 0 1-14 0v-1" />
      <line x1="12" x2="12" y1="18" y2="22" />
      <line x1="8" x2="16" y1="22" y2="22" />
    </svg>
  );
}

export function VoiceRecorder({
  sessionId,
  label,
  disabled = false,
  variant = "default",
  onMessage,
  onEnded,
}: VoiceRecorderProps) {
  const { t } = useTranslation();
  const { isRecording, startRecording, stopRecording, error: recorderError } =
    useVoiceRecorder();
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const resolvedLabel = label ?? t("chat.recordVoice");

  const handleToggle = useCallback(async () => {
    if (disabled || !sessionId) return;

    if (!isRecording) {
      await startRecording();
      return;
    }

    setIsSending(true);
    setError(null);

    const blob = await stopRecording();
    if (!blob) {
      setIsSending(false);
      return;
    }

    try {
      const response = await sendVoiceMessage(blob, sessionId);
      const transcript = response.transcript ?? "";
      onMessage([
        createMessage(
          "user",
          transcript || t("chat.voiceMessageFallback"),
          transcript,
        ),
      ]);
      onMessage([createMessage("assistant", response.response)]);

      if (response.ended) {
        onEnded();
      }
    } catch (err) {
      setError(
        err instanceof Error ? err.message : t("chat.sendRecordingError"),
      );
    } finally {
      setIsSending(false);
    }
  }, [
    disabled,
    sessionId,
    isRecording,
    startRecording,
    stopRecording,
    onMessage,
    onEnded,
    t,
  ]);

  const displayError = error ?? recorderError;
  const recordButtonClass = [
    styles.recordButton,
    isRecording ? styles.recording : "",
  ]
    .filter(Boolean)
    .join(" ");

  const ariaLabel = isRecording ? t("chat.stopRecording") : resolvedLabel;

  const button = (
    <button
      type="button"
      className={recordButtonClass}
      disabled={disabled || isSending || !sessionId}
      aria-label={ariaLabel}
      title={displayError ?? (isRecording ? t("chat.recording") : resolvedLabel)}
      onClick={handleToggle}
    >
      <MicrophoneIcon />
    </button>
  );

  if (variant === "inline") {
    return (
      <div className={styles.inline}>
        {button}
        {isRecording && (
          <span className={styles.srOnly} role="status" aria-live="polite">
            {t("chat.recording")}
          </span>
        )}
      </div>
    );
  }

  return (
    <section className={styles.section}>
      <p className={styles.label}>{resolvedLabel}</p>
      {button}
      {isRecording && <p className={styles.status}>{t("chat.recording")}</p>}
      {displayError && <p className={styles.error}>{displayError}</p>}
    </section>
  );
}
