export interface Comment {
  id: string;
  eventId: string;
  userId: string;
  content: string;
  createdAt: Date;
  likes: number;
  replies: Reply[];
  user?: {
    name: string;
    avatar: string;
  };
  timestamp?: Date;
}

export interface Reply {
  id: string;
  userId: string;
  content: string;
  createdAt: Date;
  likes: number;
  user: {
    name: string;
    avatar: string;
  };
}