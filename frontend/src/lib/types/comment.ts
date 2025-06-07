export type CommentStatus = 'active' | 'deleted' | 'hidden';

export interface Comment {
  $id: string;
  $createdAt: string;
  $updatedAt: string;
  event_id: string;
  user_id: string;
  author_name: string;
  author_avatar?: string;
  content: string;
  parent_id?: string;
  likes: number;
  is_edited: boolean;
  paid_amount?: string;
  status: CommentStatus;
  isLiked?: boolean;
  replies?: Comment[];
  timestamp?: Date; // 用于前端显示
}

// 用于API响应的评论类型，包含嵌套回复
export interface CommentWithReplies extends Comment {
  replies: Comment[];
}