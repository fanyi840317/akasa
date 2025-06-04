<script lang="ts">
  import { fade } from "svelte/transition";
  import { createEventDispatcher, onMount } from "svelte";
  import { Smile, ThumbsUp, ThumbsDown, ChevronDown, MoreVertical, Loader2, ListFilter } from "lucide-svelte";
  import { formatDistanceToNow } from "date-fns";
  import { zhCN } from "date-fns/locale";
  import { cn } from "$lib/utils";
  import { UserAvatar } from "$lib/components/ui/avatar";
  import { commentStore } from "$lib/stores/comment";
  import { auth } from "$lib/stores/auth";
  import { toast } from "svelte-sonner";
  import type { Comment, CommentWithReplies } from "$lib/types/comment";

  const dispatch = createEventDispatcher();

  let {
    eventId = $bindable(""),
    class: className,
    ...restProps
  } = $props<{
    eventId: string;
    class?: string;
  }>();

  // 评论状态
  let comments: CommentWithReplies[] = $state([]);
  let loading = $state(false);
  let error = $state<string | null>(null);
  
  // 新评论内容
  let newComment = $state("");
  let showCommentInputButtons = $state(false);
  let submittingComment = $state(false);

  // 格式化时间
  function formatTimestamp(dateStr?: string): string {
    if(!dateStr) return '未知';
    const date = new Date(dateStr);
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
  async function handleAddComment() {
    if (!newComment.trim()) return;
    if (!$auth.user) {
      toast.error("请先登录");
      return;
    }
    
    submittingComment = true;
    try {
      await commentStore.addComment({
        event_id: eventId,
        user_id: $auth.user.$id,
        author_name: $auth.user.name || '匿名用户',
        author_avatar: $auth.user.prefs?.avatar || '',
        content: newComment,
        likes: 0,
        is_edited: false,
        status: 'active'
      });
      
      newComment = "";
      showCommentInputButtons = false;
    } catch (err) {
      console.error('添加评论失败:', err);
    } finally {
      submittingComment = false;
    }
  }

  function handleCancelComment() {
    newComment = "";
    showCommentInputButtons = false;
  }

  // 点赞评论
  async function handleLikeComment(commentId: string) {
    if (!$auth.user) {
      toast.error("请先登录");
      return;
    }
    
    try {
      await commentStore.likeComment(commentId);
    } catch (err) {
      console.error('点赞失败:', err);
    }
  }
  
  // 回复评论相关状态
  let activeReplyInput = $state<string | null>(null);
  let replyContent = $state("");
  let submittingReply = $state(false);
  
  // 显示回复输入框
  function showReplyInput(commentId: string) {
    activeReplyInput = commentId;
    replyContent = "";
  }
  
  // 隐藏回复输入框
  function hideReplyInput() {
    activeReplyInput = null;
    replyContent = "";
  }
   
  // 提交回复
  async function handleAddReply(parentCommentId: string) {
     if (!replyContent.trim()) return;
     if (!$auth.user) {
       toast.error("请先登录");
       return;
     }
     
     submittingReply = true;
     try {
       await commentStore.addComment({
         event_id: eventId,
         user_id: $auth.user.$id,
         author_name: $auth.user.name || '匿名用户',
         author_avatar: $auth.user.prefs?.avatar || '',
         content: replyContent,
         parent_id: parentCommentId,
         likes: 0,
         is_edited: false,
         status: 'active'
       });
       
       replyContent = "";
       activeReplyInput = null; // 关闭回复输入框
     } catch (err) {
       console.error('添加回复失败:', err);
     } finally {
       submittingReply = false;
     }
   }
   
   // 删除评论
   async function handleDeleteComment(commentId: string) {
     if (!$auth.user) {
       toast.error("请先登录");
       return;
     }
     
     if (confirm("确定要删除这条评论吗？")) {
       try {
         await commentStore.deleteComment(commentId);
       } catch (err) {
         console.error('删除评论失败:', err);
       }
     }
   }
   
   // 加载评论
   async function loadComments() {
     if (!eventId) return;
     
     loading = true;
     try {
       const result = await commentStore.fetchComments(eventId);
       comments = result;
     } catch (err) {
       console.error('加载评论失败:', err);
       error = '加载评论失败';
     } finally {
       loading = false;
     }
   }
   
   // 监听eventId变化，重新加载评论
   $effect(() => {
     if (eventId) {
       loadComments();
     }
   });

  // 显示/隐藏回复状态
  let showReplies: Record<string, boolean> = $state({});


  function toggleReplies(commentId: string) {
    showReplies[commentId] = !showReplies[commentId];
  }
</script>

<div
  class={cn(
    "w-full bg-base-100 text-base-content  p-4 py-2 font-san border-l border-base-300 w-[400px] h-[100vh] ",
    className
  )}
  {...restProps}
>


  <div class="flex items-center mb-4 justify-between">

    <h2 class="text-lg font-semibold mr-4">

      {comments.length.toLocaleString()} 条评论

    </h2>

    <div class="flex items-center gap-2">

      <button class="btn btn-ghost text-neutral-400 btn-sm">

        <ListFilter class="w-4 h-4 mr-1" />

        排序方式

      </button>

      <button class="btn btn-ghost text-neutral-400 btn-sm" onclick={() => dispatch("closeCommentsPanel")}>

        关闭

      </button>

    </div>

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
              class:bg-neutral-700={!newComment.trim() || submittingComment}
              class:text-neutral-500={!newComment.trim() || submittingComment}
              class:bg-blue-500={newComment.trim() && !submittingComment}
              class:text-white={newComment.trim() && !submittingComment}
              disabled={!newComment.trim() || submittingComment}
              onclick={handleAddComment}
            >
              {#if submittingComment}
                <Loader2 class="w-4 h-4 animate-spin mr-1" />
              {/if}
              评论
            </button>
          </div>
        </div>
      {/if}
    </div>
  </div>

  <!-- Comments List -->
  <div class="space-y-6">
    {#each comments as comment (comment.$id)}
      <div class="flex items-start group">
        <UserAvatar
          class="size-8 mr-3 "
          src={comment.author_avatar}
          fallback={comment.author_name[0]?.toUpperCase()}
        ></UserAvatar>

        <div class="flex-1">
          <div class="flex flex-row items-center text-xs mb-0.5">
            <span class="font-semibold mr-1.5">@{comment.author_name }</span>
            <span class="text-neutral-400"
              >{formatTimestamp(comment.$createdAt || undefined)}</span
            >
            {#if comment.is_edited}
              <span class="text-neutral-400 ml-1.5">(已修改)</span>
            {/if}
          </div>

          {#if comment.paid_amount}
            <div
              class="text-xs my-1 px-2 py-0.5 bg-red-600 text-white inline-block rounded-sm"
            >
              {comment.paid_amount}
            </div>
          {/if}

          <p class="text-xs leading-relaxed whitespace-pre-wrap">
            {comment.content}
          </p>

          <div class="flex items-center gap-2 mt-1.5 text-neutral-400">
            <button
              class="flex items-center hover:text-white p-1 rounded-full hover:bg-neutral-800"
              onclick={() => handleLikeComment(comment.$id)}
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
              onclick={() => showReplyInput(comment.$id)}
            >
              回复
            </button>
            {#if $auth.user && ($auth.user.$id === comment.user_id )}
              <button
                class="text-xs font-semibold hover:text-white p-1 rounded-full hover:bg-neutral-800 text-red-400 hover:text-red-300"
                onclick={() => handleDeleteComment(comment.$id)}
              >
                删除
              </button>
            {/if}
          </div>

          <!-- Reply Input -->
          {#if activeReplyInput === comment.$id}
            <div class="flex items-start mt-3 ml-3">
              <UserAvatar 
                class="size-8 mt-1 mr-2" 
                src={$auth.user?.prefs["avatar"] || ""}
                fallback={$auth.user?.name?.[0]?.toUpperCase() || "U"}
              ></UserAvatar>
              <div class="flex-1">
                <textarea
                  placeholder={`回复 @${comment.author_name}...`}
                  bind:value={replyContent}
                  class="w-full bg-transparent border-b border-neutral-700 focus:border-white outline-none resize-none py-1 text-xs placeholder-neutral-500"
                  rows={1}
                ></textarea>
                <div class="flex justify-end items-center mt-1.5">
                  <button
                    class="px-3 py-1 text-xs text-neutral-400 hover:bg-neutral-700 rounded-full mr-1.5"
                    onclick={() => hideReplyInput()}
                  >
                    取消
                  </button>
                  <button
                    class="px-3 py-1 text-xs rounded-full transition-colors duration-200"
                    class:bg-neutral-700={!replyContent.trim() || submittingReply}
                    class:text-neutral-500={!replyContent.trim() || submittingReply}
                    class:bg-blue-500={replyContent.trim() && !submittingReply}
                    class:text-white={replyContent.trim() && !submittingReply}
                    disabled={!replyContent.trim() || submittingReply}
                    onclick={() => handleAddReply(comment.$id)}
                  >
                    {#if submittingReply}
                      <Loader2 class="w-3 h-3 animate-spin mr-1" />
                    {/if}
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
              onclick={() => toggleReplies(comment.$id)}
            >
              <ChevronDown
                class="w-4 h-4 mr-1 transition-transform duration-200 {!!showReplies[comment.$id] ? 'rotate-180' : ''}"
              />
              {comment.replies.length} 条回复
            </button>
            {#if showReplies[comment.$id ]}
              <div
                class="ml-3 mt-3 space-y-4 border-l-2 border-neutral-800 pl-4"
              >
                {#each comment.replies as reply (reply.$id )}
                  <div class="flex items-start group">
                    <UserAvatar
                      class="size-6 mt-1 mr-2 "
                      fallbackClass="text-xs"
                      src={reply.author_avatar }
                      fallback={(reply.author_name  || "U")[0]?.toUpperCase()}
                    ></UserAvatar>

                    <div class="flex-1">
                      <div class="flex items-center text-[10px] mb-0.5">
                        <span class="font-semibold mr-1.5"
                          >@{reply.author_name }</span
                        >
                        <span class="text-neutral-400"
                          >{formatTimestamp(reply.$createdAt )}</span
                        >
                        {#if reply.is_edited}
                          <span class="text-neutral-400 ml-1.5">(已修改)</span>
                        {/if}
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
                            handleLikeComment(reply.$id )}
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
                          onclick={() => showReplyInput(reply.$id )}
                        >
                          回复
                        </button>
                        {#if $auth.user && ($auth.user.$id === reply.user_id )}
                          <button
                            class="text-xs font-semibold hover:text-white p-1 rounded-full hover:bg-neutral-800 text-red-400 hover:text-red-300"
                            onclick={() => handleDeleteComment(reply.$id )}
                          >
                            删除
                          </button>
                        {/if}
                      </div>
                      <!-- Reply Input for replies -->
                      {#if activeReplyInput === (reply.$id )}
                        <div class="flex items-start mt-3 ml-3">
                          <UserAvatar 
                            class="size-6 mt-1 mr-2" 
                            fallbackClass="text-xs"
                            src={$auth.user?.prefs["avatar"] || ""}
                            fallback={$auth.user?.name?.[0]?.toUpperCase() || "U"}
                          ></UserAvatar>
                          <div class="flex-1">
                            <textarea
                              placeholder={`回复 @${reply.author_name }...`}
                              bind:value={replyContent}
                              class="w-full bg-transparent border-b border-neutral-700 focus:border-white outline-none resize-none py-1 text-xs placeholder-neutral-500"
                              rows={1}
                            ></textarea>
                            <div class="flex justify-end items-center mt-1.5">
                              <button
                                class="px-3 py-1 text-xs text-neutral-400 hover:bg-neutral-700 rounded-full mr-1.5"
                                onclick={() => hideReplyInput()}
                              >
                                取消
                              </button>
                              <button
                                class="px-3 py-1 text-xs rounded-full transition-colors duration-200"
                                class:bg-neutral-700={!replyContent.trim() || submittingReply}
                                class:text-neutral-500={!replyContent.trim() || submittingReply}
                                class:bg-blue-500={replyContent.trim() && !submittingReply}
                                class:text-white={replyContent.trim() && !submittingReply}
                                disabled={!replyContent.trim() || submittingReply}
                                onclick={() => handleAddReply(reply.$id )}
                              >
                                {#if submittingReply}
                                  <Loader2 class="w-3 h-3 animate-spin mr-1" />
                                {/if}
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
