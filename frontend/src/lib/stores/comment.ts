import { writable, get } from 'svelte/store';
import { databases } from '../../../../web.app/src/lib/appwrite';
import { ID, Query } from 'appwrite';
import type { Comment, CommentWithReplies } from '../types/comment';
import { toast } from "svelte-sonner";
import { _ } from "svelte-i18n";
import { auth } from "./auth";

type CommentState = {
    comments: CommentWithReplies[];
    loading: boolean;
    error: string | null;
};

// 从appwrite.ts中获取配置
import { appwriteConfig } from '../../../../web.app/src/lib/appwrite';
const { databaseId } = appwriteConfig;

// 定义comments集合ID
const commentsCollectionId = 'comments';

const createCommentStore = () => {
    const { subscribe, set, update } = writable<CommentState>({
        comments: [],
        loading: false,
        error: null
    });

    return {
        subscribe,
        // 获取事件的所有评论
        fetchComments: async (eventId: string) => {
            update(state => ({ ...state, loading: true, error: null }));
            try {
                // 获取顶级评论（没有parent_id的评论）
                const response = await databases.listDocuments(
                    databaseId,
                    commentsCollectionId,
                    [
                        Query.equal('event_id', eventId),
                        Query.equal('status', 'active'),
                        Query.isNull('parent_id')
                    ]
                );

                const topLevelComments = response.documents as unknown as Comment[];
                
                // 获取所有回复（有parent_id的评论）
                const repliesResponse = await databases.listDocuments(
                    databaseId,
                    commentsCollectionId,
                    [
                        Query.equal('event_id', eventId),
                        Query.equal('status', 'active'),
                        Query.notNull('parent_id')
                    ]
                );

                const replies = repliesResponse.documents as unknown as Comment[];
                
                // 将回复添加到对应的父评论中
                const commentsWithReplies: CommentWithReplies[] = topLevelComments.map(comment => {
                    const commentReplies = replies.filter(reply => reply.parent_id === comment.$id);
                    return {
                        ...comment,
                        replies: commentReplies
                    };
                });

                update(state => ({
                    ...state,
                    comments: commentsWithReplies,
                    loading: false
                }));
                
                return commentsWithReplies;
            } catch (error: any) {
                const errorMessage = error.message || '获取评论失败';
                update(state => ({ ...state, loading: false, error: errorMessage }));
                toast.error(errorMessage);
                return [];
            }
        },

        // 添加新评论
        addComment: async (comment: Omit<Comment, '$id' | '$createdAt' | '$updatedAt'>) => {
            update(state => ({ ...state, loading: true, error: null }));
            try {
                const currentUser = get(auth).user;
                if (!currentUser) {
                    throw new Error('用户未登录');
                }

                const newComment = await databases.createDocument(
                    databaseId,
                    commentsCollectionId,
                    ID.unique(),
                    {
                        ...comment,
                        user_id: currentUser.$id,
                        author_name: currentUser.name || '匿名用户',
                        author_avatar: currentUser.prefs?.avatar || '',
                        likes: 0,
                        is_edited: false,
                        status: 'active'
                    }
                );

                // 如果是回复，更新父评论的回复列表
                if (comment.parent_id) {
                    update(state => {
                        const updatedComments = state.comments.map(parentComment => {
                            if (parentComment.$id === comment.parent_id) {
                                return {
                                    ...parentComment,
                                    replies: [...(parentComment.replies || []), newComment as unknown as Comment]
                                };
                            }
                            return parentComment;
                        });
                        return { ...state, comments: updatedComments, loading: false };
                    });
                } else {
                    // 如果是顶级评论，添加到评论列表
                    update(state => ({
                        ...state,
                        comments: [...state.comments, { ...newComment, replies: [] } as unknown as CommentWithReplies],
                        loading: false
                    }));
                }

                toast.success(get(_)('comment.added'));
                return newComment as unknown as Comment;
            } catch (error: any) {
                const errorMessage = error.message || '添加评论失败';
                update(state => ({ ...state, loading: false, error: errorMessage }));
                toast.error(errorMessage);
                throw error;
            }
        },

        // 更新评论
        updateComment: async (commentId: string, content: string) => {
            update(state => ({ ...state, loading: true, error: null }));
            try {
                const updatedComment = await databases.updateDocument(
                    databaseId,
                    commentsCollectionId,
                    commentId,
                    {
                        content,
                        is_edited: true
                    }
                );

                // 更新状态中的评论
                update(state => {
                    const updatedComments = state.comments.map(comment => {
                        if (comment.$id === commentId) {
                            return { ...comment, content, is_edited: true };
                        }
                        
                        // 检查回复中是否有需要更新的评论
                        if (comment.replies && comment.replies.length > 0) {
                            const updatedReplies = comment.replies.map(reply => {
                                if (reply.$id === commentId) {
                                    return { ...reply, content, is_edited: true };
                                }
                                return reply;
                            });
                            return { ...comment, replies: updatedReplies };
                        }
                        
                        return comment;
                    });
                    return { ...state, comments: updatedComments, loading: false };
                });

                toast.success(get(_)('comment.updated'));
                return updatedComment as unknown as Comment;
            } catch (error: any) {
                const errorMessage = error.message || '更新评论失败';
                update(state => ({ ...state, loading: false, error: errorMessage }));
                toast.error(errorMessage);
                throw error;
            }
        },

        // 删除评论（软删除，将状态设置为deleted）
        deleteComment: async (commentId: string) => {
            update(state => ({ ...state, loading: true, error: null }));
            try {
                await databases.updateDocument(
                    databaseId,
                    commentsCollectionId,
                    commentId,
                    {
                        status: 'deleted'
                    }
                );

                // 从状态中移除评论
                update(state => {
                    // 检查是否为顶级评论
                    const isTopLevel = state.comments.some(comment => comment.$id === commentId);
                    
                    if (isTopLevel) {
                        // 移除顶级评论
                        const updatedComments = state.comments.filter(comment => comment.$id !== commentId);
                        return { ...state, comments: updatedComments, loading: false };
                    } else {
                        // 从回复中移除评论
                        const updatedComments = state.comments.map(comment => {
                            if (comment.replies && comment.replies.length > 0) {
                                return {
                                    ...comment,
                                    replies: comment.replies.filter(reply => reply.$id !== commentId)
                                };
                            }
                            return comment;
                        });
                        return { ...state, comments: updatedComments, loading: false };
                    }
                });

                toast.success(get(_)('comment.deleted'));
                return true;
            } catch (error: any) {
                const errorMessage = error.message || '删除评论失败';
                update(state => ({ ...state, loading: false, error: errorMessage }));
                toast.error(errorMessage);
                throw error;
            }
        },

        // 点赞评论
        likeComment: async (commentId: string) => {
            try {
                // 获取当前评论
                const comment = await databases.getDocument(
                    databaseId,
                    commentsCollectionId,
                    commentId
                ) as unknown as Comment;

                // 增加点赞数
                const updatedComment = await databases.updateDocument(
                    databaseId,
                    commentsCollectionId,
                    commentId,
                    {
                        likes: (comment.likes || 0) + 1
                    }
                );

                // 更新状态中的评论点赞数
                update(state => {
                    const updatedComments = state.comments.map(comment => {
                        if (comment.$id === commentId) {
                            return { ...comment, likes: (comment.likes || 0) + 1, isLiked: true };
                        }
                        
                        // 检查回复中是否有需要更新的评论
                        if (comment.replies && comment.replies.length > 0) {
                            const updatedReplies = comment.replies.map(reply => {
                                if (reply.$id === commentId) {
                                    return { ...reply, likes: (reply.likes || 0) + 1, isLiked: true };
                                }
                                return reply;
                            });
                            return { ...comment, replies: updatedReplies };
                        }
                        
                        return comment;
                    });
                    return { ...state, comments: updatedComments };
                });

                return updatedComment as unknown as Comment;
            } catch (error: any) {
                const errorMessage = error.message || '点赞失败';
                toast.error(errorMessage);
                throw error;
            }
        },

        // 清空评论列表
        clearComments: () => {
            set({
                comments: [],
                loading: false,
                error: null
            });
        }
    };
};

export const commentStore = createCommentStore();