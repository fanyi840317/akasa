<script lang="ts">
  import { fade } from "svelte/transition";
  import { createEventDispatcher, onMount } from "svelte";
  import {
    MessageSquare,
    Send,
    ThumbsUp,
    ThumbsDown,
    Reply,
    Smile,
    MoreVertical,
    ChevronDown,
    ListFilter,
  } from "lucide-svelte"; // Added ThumbsDown, Smile, MoreVertical, ChevronDown, ListFilter
  import { cn } from "$lib/utils";
  import { UserAvatar } from "$lib/components/ui/avatar";

  const dispatch = createEventDispatcher();

  // 评论类型定义
  interface Comment {
    id: string;
    author: {
      name: string;
      avatar?: string;
    };
    content: string;
    timestamp: Date;
    likes: number;
    dislikes?: number; // Added dislikes
    replies?: Comment[];
    isEdited?: boolean; // Added isEdited
    paidAmount?: string; // Added paidAmount
  }

  let {
    comments = $bindable([]),
    eventId = $bindable(""),
    class: className,
    ...restProps
  } = $props<{
    comments: Comment[];
    eventId: string;
    class?: string;
  }>();

  // 新评论内容
  let newComment = $state("");
  let showCommentInputButtons = $state(false);

  // 格式化时间
  function formatTimestamp(date: Date): string {
    const now = new Date();
    const diff = now.getTime() - date.getTime();

    if (diff < 60 * 1000) return "刚刚";
    if (diff < 60 * 60 * 1000) return `${Math.floor(diff / (60 * 1000))}分钟前`;
    if (diff < 24 * 60 * 60 * 1000)
      return `${Math.floor(diff / (60 * 60 * 1000))}小时前`;
    if (diff < 30 * 24 * 60 * 60 * 1000)
      return `${Math.floor(diff / (24 * 60 * 60 * 1000))}天前`;
    return date.toLocaleDateString("zh-CN", {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  }

  // 添加评论
  function handleAddComment() {
    if (!newComment.trim()) return;
    const comment: Comment = {
      id: crypto.randomUUID(),
      author: { name: "当前用户", avatar: "/images/avatars/user.png" }, // Replace with actual user data
      content: newComment,
      timestamp: new Date(),
      likes: 0,
      replies: [],
    };
    comments = [comment, ...comments];
    dispatch("commentAdded", { comment });
    newComment = "";
    showCommentInputButtons = false;
  }

  function handleCancelComment() {
    newComment = "";
    showCommentInputButtons = false;
  }

  // 点赞评论
  function handleLikeComment(
    commentId: string,
    isReply = false,
    parentCommentId?: string
  ) {
    const updateLikes = (items: Comment[]) => {
      return items.map((item) => {
        if (item.id === commentId) {
          return { ...item, likes: (item.likes || 0) + 1 };
        }
        if (item.replies && item.replies.length > 0) {
          return { ...item, replies: updateLikes(item.replies) };
        }
        return item;
      });
    };
    comments = updateLikes(comments);
    dispatch("commentLiked", { commentId, isReply, parentCommentId });
  }

  // 回复评论
  function handleReplyComment(commentId: string) {
    dispatch("commentReply", { commentId });
  }

  let activeReplyInput: string | null = $state(null);
  let replyContent = $state("");

  function toggleReplyInput(commentId: string) {
    if (activeReplyInput === commentId) {
      activeReplyInput = null;
    } else {
      activeReplyInput = commentId;
      replyContent = ""; // Reset reply content when opening a new input
    }
  }

  function submitReply(parentCommentId: string) {
    if (!replyContent.trim()) return;

    const newReply: Comment = {
      id: crypto.randomUUID(),
      author: { name: "当前用户", avatar: "/images/avatars/user.png" }, // Replace with actual user data
      content: replyContent,
      timestamp: new Date(),
      likes: 0,
    };

    const addReplyRecursively = (items: Comment[]): Comment[] => {
      return items.map((comment) => {
        if (comment.id === parentCommentId) {
          return {
            ...comment,
            replies: [...(comment.replies || []), newReply],
          };
        }
        if (comment.replies && comment.replies.length > 0) {
          return { ...comment, replies: addReplyRecursively(comment.replies) };
        }
        return comment;
      });
    };

    comments = addReplyRecursively(comments);
    dispatch("replyAdded", { parentCommentId, reply: newReply });
    replyContent = "";
    activeReplyInput = null; // Close input after submitting
  }

  onMount(() => {
    if (comments.length === 0) {
      comments = [
        {
          id: "1",
          author: { name: "wafsn2218", avatar: "/images/avatars/user_w.png" }, // Example avatar
          content:
            "我始终相信兼听则明，二爷的故事始终是我了解历史真相的一块拼图，不偏不倚。希望二爷可以坚持，不要像某些youtuber为了黑而黑，而是有事实有依据的真实讲述历史故事。",
          timestamp: new Date(Date.now() - 1000 * 60 * 60 * 24 * 30 * 4), // 4 months ago
          likes: 850,
          isEdited: true,
          paidAmount: "US$200.00",
          replies: [
            {
              id: "1-1",
              author: { name: "范翼", avatar: "/images/avatars/user_fan.png" },
              content: "说得好！",
              timestamp: new Date(Date.now() - 1000 * 60 * 60 * 24 * 30 * 3), // 3 months ago
              likes: 10,
            },
          ],
        },
        {
          id: "2",
          author: {
            name: "riverhe2853",
            avatar: "/images/avatars/user_dog.png",
          },
          content: "谢谢精彩视频，祝二爷一家新年快乐🎉🎊",
          timestamp: new Date(Date.now() - 1000 * 60 * 60 * 24 * 30 * 4), // 4 months ago
          likes: 23,
          paidAmount: "CA$5.00",
          replies: [],
        },
      ];
    }
  });

  let showReplies: Record<string, boolean> = $state({});

  function toggleReplies(commentId: string) {
    showReplies[commentId] = !showReplies[commentId];
  }
</script>

<div
  class={cn(
    "w-full bg-base-200 text-white p-4 font-san border-l border-base-300 w-[400px] h-[100vh] ",
    className
  )}
  {...restProps}
>
  <div class="flex items-center mb-4">
    <h2 class="text-lg font-semibold mr-4">
      {comments.length.toLocaleString()} 条评论
    </h2>
    <button class="btn btn-ghost text-neutral-400 btn-sm">
      <ListFilter class="w-4 h-4 mr-1" />
      排序方式
    </button>
  </div>

  <!-- Add Comment Input -->
  <div class="flex items-start mb-6">
    <UserAvatar class="size-8 mt-1 mr-3 " fallback="范"></UserAvatar>
    <!-- <div class="avatar mr-3">
      <div class="w-10 h-10 rounded-full bg-blue-500 flex items-center justify-center text-white text-lg font-semibold">
        范
      </div>
    </div> -->
    <div class="flex-1">
      <textarea
        placeholder="添加评论..."
        bind:value={newComment}
        onfocus={() => (showCommentInputButtons = true)}
        class="w-full bg-transparent border-b border-neutral-700 focus:border-white
         outline-none resize-none py-2 text-xs placeholder-neutral-500"
        rows="1"
      ></textarea>
      {#if showCommentInputButtons}
        <div class="flex justify-between items-center mt-2">
          <Smile
            class="size-4 text-neutral-400 hover:text-white cursor-pointer"
          />
          <div class="flex gap-2">
            <button
              class="btn btn-sm btn-ghost text-neutral-400 hover:text-white"
              onclick={handleCancelComment}
            >
              取消
            </button>
            <button
              class="btn btn-sm transition-colors duration-200"
              class:bg-neutral-700={!newComment.trim()}
              class:text-neutral-500={!newComment.trim()}
              class:bg-blue-500={newComment.trim()}
              class:text-white={newComment.trim()}
              disabled={!newComment.trim()}
              onclick={handleAddComment}
            >
              评论
            </button>
          </div>
        </div>
      {/if}
    </div>
  </div>

  <!-- Comments List -->
  <div class="space-y-6">
    {#each comments as comment (comment.id)}
      <div class="flex items-start group">
        <UserAvatar
          class="size-8 mr-3 "
          src={comment.author.avatar}
          fallback={comment.author.name[0]?.toUpperCase()}
        ></UserAvatar>

        <div class="flex-1">
          <div class="flex flex-row items-center text-xs mb-0.5">
            <span class="font-semibold mr-1.5">@{comment.author.name}</span>
            <span class="text-neutral-400"
              >{formatTimestamp(comment.timestamp)}</span
            >
          </div>

          <!-- {#if comment.paidAmount}
            <div
              class="text-xs my-1 px-2 py-0.5 bg-red-600 text-white inline-block rounded-sm"
            >
              {comment.paidAmount}
            </div>
          {/if} -->

          <p class="text-xs leading-relaxed whitespace-pre-wrap">
            {comment.content}
          </p>

          <div class="flex items-center gap-2 mt-1.5 text-neutral-400">
            <button
              class="flex items-center hover:text-white p-1 rounded-full hover:bg-neutral-800"
              onclick={() => handleLikeComment(comment.id)}
            >
              <ThumbsUp class="w-4 h-4" />
              {#if comment.likes > 0}<span class="text-xs ml-1"
                  >{comment.likes}</span
                >{/if}
            </button>
            <button
              class="hover:text-white p-1 rounded-full hover:bg-neutral-800"
            >
              <ThumbsDown class="w-4 h-4" />
            </button>
            <button
              class="text-xs font-semibold hover:text-white p-1 rounded-full hover:bg-neutral-800"
              onclick={() => toggleReplyInput(comment.id)}
            >
              回复
            </button>
          </div>

          <!-- Reply Input -->
          {#if activeReplyInput === comment.id}
            <div class="flex items-start mt-3 ml-3">
              <UserAvatar class="size-8 mt-1 mr-2 " fallback="范"></UserAvatar>
              <div class="flex-1">
                <textarea
                  placeholder={`回复 @${comment.author.name}...`}
                  bind:value={replyContent}
                  class="w-full bg-transparent border-b border-neutral-700 focus:border-white outline-none resize-none py-1 text-xs placeholder-neutral-500"
                  rows={1}
                ></textarea>
                <div class="flex justify-end items-center mt-1.5">
                  <button
                    class="px-3 py-1 text-xs text-neutral-400 hover:bg-neutral-700 rounded-full mr-1.5"
                    onclick={() => (activeReplyInput = null)}
                  >
                    取消
                  </button>
                  <button
                    class="px-3 py-1 text-xs rounded-full transition-colors duration-200"
                    class:bg-neutral-700={!replyContent.trim()}
                    class:text-neutral-500={!replyContent.trim()}
                    class:bg-blue-500={replyContent.trim()}
                    class:text-white={replyContent.trim()}
                    disabled={!replyContent.trim()}
                    onclick={() => submitReply(comment.id)}
                  >
                    回复
                  </button>
                </div>
              </div>
            </div>
          {/if}

          <!-- Replies List -->
          {#if comment.replies && comment.replies.length > 0}
            <button
              class="flex items-center text-blue-400 text-xs font-semibold mt-2 hover:bg-blue-400 hover:bg-opacity-20 p-1.5 rounded-full"
              onclick={() => toggleReplies(comment.id)}
            >
              <ChevronDown
                class="w-4 h-4 mr-1 transition-transform duration-200"
              />
              {comment.replies.length} 条回复
            </button>
            {#if showReplies[comment.id]}
              <div
                class="ml-3 mt-3 space-y-4 border-l-2 border-neutral-800 pl-4"
              >
                {#each comment.replies as reply (reply.id)}
                  <div class="flex items-start group">
                    <UserAvatar
                      class="size-6 mt-1 mr-2 "
                      fallbackClass="text-xs"
                      src={reply.author.avatar}
                      fallback={reply.author.name[0]?.toUpperCase()}
                    ></UserAvatar>

                    <div class="flex-1">
                      <div class="flex items-center text-[10px] mb-0.5">
                        <span class="font-semibold mr-1.5"
                          >@{reply.author.name}</span
                        >
                        <span class="text-neutral-400"
                          >{formatTimestamp(reply.timestamp)}</span
                        >
                        <!-- {#if reply.isEdited}
                          <span class="text-neutral-400 ml-1.5">(已修改)</span>
                        {/if} -->
                      </div>
                
                      <p class="text-xs leading-relaxed whitespace-pre-wrap">
                        {reply.content}
                      </p>
                      <div
                        class="flex items-center gap-2 mt-1.5 text-neutral-400"
                      >
                        <button
                          class="flex items-center hover:text-white p-1 rounded-full hover:bg-neutral-800"
                          onclick={() =>
                            handleLikeComment(reply.id, true, comment.id)}
                        >
                          <ThumbsUp class="w-4 h-4" />
                          {#if reply.likes > 0}<span class="text-xs ml-1"
                              >{reply.likes}</span
                            >{/if}
                        </button>
                        <button
                          class="hover:text-white p-1 rounded-full hover:bg-neutral-800"
                        >
                          <ThumbsDown class="w-4 h-4" />
                        </button>
                        <button
                          class="text-xs font-semibold hover:text-white p-1 rounded-full hover:bg-neutral-800"
                          onclick={() => toggleReplyInput(reply.id)}
                        >
                          回复
                        </button>
                      </div>
                      <!-- Reply Input for replies -->
                      {#if activeReplyInput === reply.id}
                        <div class="flex items-start mt-3 ml-3">
                          <div class="avatar mr-2">
                            <div
                              class="w-6 h-6 rounded-full bg-blue-500 flex items-center justify-center text-white text-sm font-semibold"
                            >
                              范
                            </div>
                          </div>
                          <div class="flex-1">
                            <textarea
                              placeholder={`回复 @${reply.author.name}...`}
                              bind:value={replyContent}
                              class="w-full bg-transparent border-b border-neutral-700 focus:border-white outline-none resize-none py-1 text-sm placeholder-neutral-500"
                              rows={1}
                            ></textarea>
                            <div class="flex justify-end items-center mt-1.5">
                              <button
                                class="px-3 py-1 text-xs text-neutral-400 hover:bg-neutral-700 rounded-full mr-1.5"
                                onclick={() => (activeReplyInput = null)}
                              >
                                取消
                              </button>
                              <button
                                class="px-3 py-1 text-xs rounded-full transition-colors duration-200"
                                class:bg-neutral-700={!replyContent.trim()}
                                class:text-neutral-500={!replyContent.trim()}
                                class:bg-blue-500={replyContent.trim()}
                                class:text-white={replyContent.trim()}
                                disabled={!replyContent.trim()}
                                onclick={() => submitReply(reply.id)}
                              >
                                回复
                              </button>
                            </div>
                          </div>
                        </div>
                      {/if}
                    </div>
                  </div>
                {/each}
              </div>
            {/if}
          {/if}
        </div>
        <button
          class="text-neutral-500 hover:text-white opacity-0 group-hover:opacity-100 transition-opacity p-1"
        >
          <MoreVertical class="w-4 h-4" />
        </button>
      </div>
    {/each}
  </div>
</div>
