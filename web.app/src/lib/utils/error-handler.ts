import { toast } from "svelte-sonner";

export class EventError extends Error {
  constructor(message: string, public code: string) {
    super(message);
    this.name = 'EventError';
  }
}

export function handleEventError(error: unknown): void {
  if (error instanceof EventError) {
    switch (error.code) {
      case 'VALIDATION_ERROR':
        toast.error(error.message);
        break;
      case 'UPLOAD_ERROR':
        toast.error('上传失败，请重试');
        break;
      case 'PUBLISH_ERROR':
        toast.error('发布失败，请重试');
        break;
      default:
        toast.error('发生错误，请重试');
    }
  } else {
    console.error('Unexpected error:', error);
    toast.error('发生未知错误，请重试');
  }
}

export function validateEvent(event: any): void {
  if (!event?.title) {
    throw new EventError('标题不能为空', 'VALIDATION_ERROR');
  }
  if (!event?.content) {
    throw new EventError('内容不能为空', 'VALIDATION_ERROR');
  }
} 