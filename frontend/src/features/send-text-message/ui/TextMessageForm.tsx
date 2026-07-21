import { FormEvent, KeyboardEvent, useState } from "react";
import { useTranslation } from "react-i18next";
import styles from "./TextMessageForm.module.css";

interface TextMessageFormProps {
  placeholder?: string;
  label?: string;
  disabled?: boolean;
  variant?: "default" | "composer";
  onSubmit: (text: string) => void;
}

function SendIcon() {
  return (
    <svg
      width="20"
      height="20"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <path d="m22 2-7 20-4-9-9-4Z" />
      <path d="M22 2 11 13" />
    </svg>
  );
}

export function TextMessageForm({
  placeholder,
  label,
  disabled = false,
  variant = "default",
  onSubmit,
}: TextMessageFormProps) {
  const { t } = useTranslation();
  const [text, setText] = useState("");
  const resolvedLabel = label ?? t("chat.sendMessage");
  const resolvedPlaceholder = placeholder ?? t("chat.placeholder");

  const submit = () => {
    if (!text.trim() || disabled) return;
    onSubmit(text);
    setText("");
  };

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    submit();
  };

  const handleKeyDown = (event: KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      submit();
    }
  };

  const isComposer = variant === "composer";
  const formClass = isComposer ? styles.composerForm : styles.form;
  const canSend = !disabled && text.trim().length > 0;

  return (
    <form className={formClass} onSubmit={handleSubmit}>
      <label
        className={isComposer ? styles.srOnly : styles.label}
        htmlFor="text-message"
      >
        {resolvedLabel}
      </label>

      <div className={isComposer ? styles.composerRow : styles.fieldGroup}>
        <textarea
          id="text-message"
          className={isComposer ? styles.composerInput : styles.textarea}
          rows={isComposer ? 1 : 3}
          value={text}
          placeholder={resolvedPlaceholder}
          disabled={disabled}
          onChange={(event) => setText(event.target.value)}
          onKeyDown={handleKeyDown}
        />

        <button
          type="submit"
          className={isComposer ? styles.sendButton : styles.defaultSendButton}
          disabled={!canSend}
          aria-label={t("chat.sendMessage")}
          title={t("chat.sendHint")}
        >
          <SendIcon />
          {!isComposer && <span>{t("chat.send")}</span>}
        </button>
      </div>
    </form>
  );
}
