import { useTranslation } from "react-i18next";
import type { Message } from "../model/types";
import styles from "./MessageItem.module.css";

interface MessageItemProps {
  message: Message;
  compact?: boolean;
}

export function MessageItem({ message, compact = false }: MessageItemProps) {
  const { t } = useTranslation();
  const isUser = message.role === "user";
  const roleClass = isUser ? styles.user : styles.assistant;

  return (
    <article className={`${styles.message} ${roleClass}`}>
      {!compact && (
        <span className={styles.role}>
          {isUser ? t("chat.roles.user") : t("chat.roles.assistant")}
        </span>
      )}
      <div className={styles.bubble}>
        <p>{message.content}</p>
        {message.transcript && message.transcript !== message.content && (
          <p className={styles.transcript}>
            {t("chat.transcript", { text: message.transcript })}
          </p>
        )}
      </div>
    </article>
  );
}
