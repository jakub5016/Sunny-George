import { useEffect, useRef } from "react";
import type { Message } from "@entities/message";
import { MessageItem } from "@entities/message/ui/MessageItem";
import styles from "./ChatWindow.module.css";

interface ChatWindowProps {
  messages: Message[];
  label?: string;
  variant?: "default" | "embedded";
  compact?: boolean;
}

export function ChatWindow({
  messages,
  label = "Conversation",
  variant = "default",
  compact = false,
}: ChatWindowProps) {
  const scrollRef = useRef<HTMLDivElement>(null);
  const isEmbedded = variant === "embedded";

  useEffect(() => {
    const container = scrollRef.current;
    if (!container) return;
    container.scrollTop = container.scrollHeight;
  }, [messages]);

  const content = messages.length === 0 ? (
    <p className={styles.empty}>
      Ask Sunny George about solar panels, savings, or installation.
    </p>
  ) : (
    <div className={styles.messages}>
      {messages.map((message) => (
        <MessageItem key={message.id} message={message} compact={compact} />
      ))}
    </div>
  );

  if (isEmbedded) {
    return (
      <div
        ref={scrollRef}
        className={styles.embedded}
        role="log"
        aria-live="polite"
        aria-label={label}
      >
        {content}
      </div>
    );
  }

  return (
    <section className={styles.section} aria-label={label}>
      <h2>{label}</h2>
      <div ref={scrollRef} className={styles.card} role="log" aria-live="polite">
        {content}
      </div>
    </section>
  );
}
