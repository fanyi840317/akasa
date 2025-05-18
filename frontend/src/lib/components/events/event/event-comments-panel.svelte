<script lang="ts">

  import { fade } from "svelte/transition";
  import { createEventDispatcher } from "svelte";
  import { MessageSquare, Send, ThumbsUp, Reply } from "lucide-svelte";
  import {cn} from "$lib/utils"
  
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
    replies?: Comment[];
  }

  let { 
    comments = $bindable([]),
    eventId = $bindable(""),
    class:className ,
  } = $props<{
    comments: Comment[];
    eventId: string;
    class?: string;
  }>();

  // 新评论内容
  let newComment = $state("");
  
  // 格式化时间
  function formatTimestamp(date: Date): string {
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    
    // 小于1分钟
    if (diff < 60 * 1000) {
      return "刚刚";
    }
    
    // 小于1小时
    if (diff < 60 * 60 * 1000) {
      const minutes = Math.floor(diff / (60 * 1000));
      return `${minutes}分钟前`;
    }
    
    // 小于24小时
    if (diff < 24 * 60 * 60 * 1000) {
      const hours = Math.floor(diff / (60 * 60 * 1000));
      return `${hours}小时前`;
    }
    
    // 小于30天
    if (diff < 30 * 24 * 60 * 60 * 1000) {
      const days = Math.floor(diff / (24 * 60 * 60 * 1000));
      return `${days}天前`;
    }
    
    // 其他情况显示完整日期
    return date.toLocaleDateString("zh-CN", {
      year: "numeric",
      month: "short",
      day: "numeric"
    });
  }

  // 添加评论
  function handleAddComment() {
    if (!newComment.trim()) return;
    
    const comment: Comment = {
      id: crypto.randomUUID(),
      author: {
        name: "当前用户",
        avatar: "/images/avatars/user.png"
      },
      content: newComment,
      timestamp: new Date(),
      likes: 0,
      replies: []
    };
    
    comments = [comment, ...comments];
    dispatch("commentAdded", { comment });
    
    // 清空输入框
    newComment = "";
  }

  // 点赞评论
  function handleLikeComment(commentId: string) {
    comments = comments.map(comment => {
      if (comment.id === commentId) {
        return { ...comment, likes: comment.likes + 1 };
      }
      return comment;
    });
    
    dispatch("commentLiked", { commentId });
  }

  // 回复评论
  function handleReplyComment(commentId: string) {
    // 这里可以实现回复功能，例如打开回复输入框
    dispatch("commentReply", { commentId });
  }
</script>

<div class={cn("card w-[280px] shadow-sm bg-neutral-900 group",className)}>
  <!-- Collapsed view: Avatars only -->
  <div class="p-3 pt-1 group-hover:hidden">
    <h2 class="card-title text-xs font-bold flex items-center gap-1 p-0 pb-2">
      <MessageSquare class="h-3 w-3" />
      <span>评论</span>
    </h2>
    {#if comments.length > 0}
    <div class="flex -space-x-2 overflow-hidden">
      {#each comments as comment (comment.id)}
        <div class="avatar">
          <div class="w-6 rounded-full border-2 border-neutral-900">
            {#if comment.author.avatar}
              <img src={comment.author.avatar} alt={comment.author.name} />
            {:else}
              <div class="bg-neutral-focus text-neutral-content flex items-center justify-center">{comment.author.name[0]}</div>
            {/if}
          </div>
        </div>
      {/each}
        <div class="w-6 h-6 rounded-full bg-neutral-focus text-neutral-content flex items-center justify-center text-xs border-2 border-neutral-900">
          +{comments.length}
        </div>
    </div>
    {:else}
    <div class="flex items-center gap-2">
      <div class="avatar placeholder">
        <div class="bg-neutral-focus text-neutral-content rounded-full w-6">
          <span class="text-xs">?</span>
        </div>
      </div>
      <span class="text-xs text-muted-foreground">添加评论...</span>
    </div>
    {/if}
  </div>

  <!-- Expanded view: Full panel -->
  <div class="card-body p-3 pt-1 space-y-3 hidden group-hover:block">
    <h2 class="card-title text-xs font-bold flex items-center gap-1 p-0 pb-2">
      <MessageSquare class="h-3 w-3" />
      <span>评论</span>
    </h2>
    <!-- 评论输入框 -->
    <div class="flex flex-col gap-2">
      <textarea
        placeholder="添加评论..."
        bind:value={newComment}
        rows={3}
        class="textarea textarea-bordered w-full resize-none text-xs"
      ></textarea>
      <div class="flex justify-end">
        <button
          class="btn btn-outline btn-sm gap-1"
          disabled={!newComment.trim()}
          onclick={handleAddComment}
        >
          <Send class="h-3 w-3" />
          <span class="text-xs">发送</span>
        </button>
      </div>
    </div>

    <div class="divider"></div>

    <!-- 评论列表 -->
    <div class="overflow-y-auto h-[400px]">
      <div class="space-y-4">
        {#if comments.length > 0}
          {#each comments as comment (comment.id)}
            <div class="flex gap-2 group" in:fade={{ duration: 200 }}>
              <div class="avatar">
                <div class="w-6 rounded-full">
                  {#if comment.author.avatar}
                    <img src={comment.author.avatar} alt={comment.author.name} />
                  {:else}
                    <div class="bg-neutral-focus text-neutral-content flex items-center justify-center">{comment.author.name[0]}</div>
                  {/if}
                </div>
              </div>

              <div class="flex-1">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-medium">{comment.author.name}</span>
                  <span class="text-xs text-muted-foreground">{formatTimestamp(comment.timestamp)}</span>
                </div>

                <p class="text-xs mt-1 break-words">{comment.content}</p>

                <div class="flex items-center gap-3 mt-2">
                  <button
                    class="btn btn-ghost btn-sm h-6 px-2 gap-1"
                    onclick={() => handleLikeComment(comment.id)}
                  >
                    <ThumbsUp class="h-3 w-3" />
                    <span class="text-xs">{comment.likes || ''}</span>
                  </button>

                  <button
                    class="btn btn-ghost btn-sm h-6 px-2 gap-1"
                    onclick={() => handleReplyComment(comment.id)}                  >
                    <Reply class="h-3 w-3" />
                    <span class="text-xs">回复</span>
                  </button>
                </div>

                <!-- 回复列表 -->
                {#if comment.replies && comment.replies.length > 0}
                  <div class="ml-4 mt-2 space-y-2 border-l-2 border-border pl-2">
                    {#each comment.replies as reply (reply.id)}
                      <div class="flex gap-2">
                        <div class="avatar">
                          <div class="w-5 rounded-full">
                            {#if reply.author.avatar}
                              <img src={reply.author.avatar} alt={reply.author.name} />
                            {:else}
                              <div class="bg-neutral-focus text-neutral-content flex items-center justify-center">{reply.author.name[0]}</div>
                            {/if}
                          </div>
                        </div>

                        <div class="flex-1">
                          <div class="flex items-center justify-between">
                            <span class="text-xs font-medium">{reply.author.name}</span>
                            <span class="text-xs text-muted-foreground">{formatTimestamp(reply.timestamp)}</span>
                          </div>
                          <p class="text-xs mt-1 break-words">{reply.content}</p>
                          <div class="flex items-center gap-3 mt-2">
                            <button
                              class="btn btn-ghost btn-sm h-6 px-2 gap-1"
                              onclick={() => handleLikeComment(reply.id)}
                            >
                              <ThumbsUp class="h-3 w-3" />
                              <span class="text-xs">{reply.likes || ''}</span>
                            </button>
                            <button
                              class="btn btn-ghost btn-sm h-6 px-2 gap-1"
                              onclick={() => handleReplyComment(reply.id)}
                            >
                              <Reply class="h-3 w-3" />
                              <span class="text-xs">回复</span>
                            </button>
                          </div>
                        </div>
                      </div>
                    {/each}
                  </div>
                {/if}
              </div>
            </div>
          {/each}
        {:else}
          <p class="text-center text-xs text-muted-foreground">暂无评论</p>
        {/if}
      </div>
    </div>
  </div>
</div>