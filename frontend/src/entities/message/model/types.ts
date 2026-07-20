export type MessageRole = "user" | "assistant";

export interface Message {
  id: string;
  role: MessageRole;
  content: string;
  transcript?: string;
}

export interface ChatResponse {
  response: string;
  session_id: string;
  ended: boolean;
  transcript: string | null;
}
