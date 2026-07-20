import { apiRequest } from "@shared/api/client";
import type { ChatResponse } from "@entities/message";
import { getApiLocale } from "@shared/lib/i18n";

export async function startChat(sessionId?: string): Promise<ChatResponse> {
  return apiRequest<ChatResponse>("/api/chat/text/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      start: true,
      session_id: sessionId,
      locale: getApiLocale(),
    }),
  });
}
