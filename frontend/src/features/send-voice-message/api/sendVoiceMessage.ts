import { apiRequest } from "@shared/api/client";
import type { ChatResponse } from "@entities/message";
import { getApiLocale } from "@shared/lib/i18n";

export async function sendVoiceMessage(
  audioBlob: Blob,
  sessionId: string,
): Promise<ChatResponse> {
  const formData = new FormData();
  formData.append("audio", audioBlob, "recording.webm");
  formData.append("session_id", sessionId);
  formData.append("locale", getApiLocale());

  return apiRequest<ChatResponse>("/api/chat/voice/", {
    method: "POST",
    body: formData,
  });
}
