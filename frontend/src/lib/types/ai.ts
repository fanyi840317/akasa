// Types
export type ChatMessage = {
    id: string;
    role: "user" | "model";
    content: string;
    timestamp: Date;
    isMarkdown?: boolean;
    actions?: Array<{
      id: string;
      label: string;
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      icon?: any;
      handler: (message: ChatMessage) => void;
    }>;
  };

export type MessageAction = {
  id: string;
  label: string;
  icon?: unknown;
  handler: (message: ChatMessage) => void;
};