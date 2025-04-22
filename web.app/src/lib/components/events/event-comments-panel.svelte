<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import { Card, CardContent, CardHeader, CardTitle } from "$lib/components/ui/card";
  import { ScrollArea } from "$lib/components/ui/scroll-area";
  import { Separator } from "$lib/components/ui/separator";
  import { Textarea } from "$lib/components/ui/textarea";
  import { Avatar, AvatarFallback, AvatarImage } from "$lib/components/ui/avatar";
  import { fade } from "svelte/transition";
  import { createEventDispatcher } from "svelte";
  import { MessageSquare, Send, ThumbsUp, Reply } from "lucide-svelte";
  
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
  } = $props<{
    comments: Comment[];
    eventId: string;
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

<Card class="shadow-sm bg-neutral-900 w-[280px]">
  <CardHeader class="p-3 pb-1">
    <CardTitle class="text-xs font-bold flex items-center gap-1">
      <MessageSquare class="h-3 w-3" />
      <span>评论</span>
    </CardTitle>
  </CardHeader>
  <CardContent class="p-3 pt-1 space-y-3">
    <!-- 评论输入框 -->
    <div class="flex flex-col gap-2">
      <Textarea 
        placeholder="添加评论..." 
        bind:value={newComment}
        rows={3}
        class="resize-none text-xs"
      />
      <div class="flex justify-end">
        <Button 
          variant="outline" 
          size="sm" 
          class="gap-1"
          disabled={!newComment.trim()}
          onclick={handleAddComment}
        >
          <Send class="h-3 w-3" />
          <span class="text-xs">发送</span>
        </Button>
      </div>
    </div>
    
    <Separator />
    
    <!-- 评论列表 -->
    <ScrollArea class="h-[400px]">
      <div class="space-y-4">
        {#if comments.length > 0}
          {#each comments as comment (comment.id)}
            <div class="flex gap-2 group" in:fade={{ duration: 200 }}>
              <Avatar class="h-6 w-6">
                {#if comment.author.avatar}
                  <AvatarImage src={comment.author.avatar} alt={comment.author.name} />
                {/if}
                <AvatarFallback>{comment.author.name[0]}</AvatarFallback>
              </Avatar>
              
              <div class="flex-1">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-medium">{comment.author.name}</span>
                  <span class="text-xs text-muted-foreground">{formatTimestamp(comment.timestamp)}</span>
                </div>
                
                <p class="text-xs mt-1 break-words">{comment.content}</p>
                
                <div class="flex items-center gap-3 mt-2">
                  <Button 
                    variant="ghost" 
                    size="sm" 
                    class="h-6 px-2 gap-1"
                    onclick={() => handleLikeComment(comment.id)}
                  >
                    <ThumbsUp class="h-3 w-3" />
                    <span class="text-xs">{comment.likes || ''}</span>
                  </Button>
                  
                  <Button 
                    variant="ghost" 
                    size="sm" 
                    class="h-6 px-2 gap-1"
                    onclick={() => handleReplyComment(comment.id)}
                  >
                    <Reply class="h-3 w-3" />
                    <span class="text-xs">回复</span>
                  </Button>
                </div>
                
                <!-- 回复列表 -->
                {#if comment.replies && comment.replies.length > 0}
                  <div class="ml-4 mt-2 space-y-2 border-l-2 border-border pl-2">
                    {#each comment.replies as reply (reply.id)}
                      <div class="flex gap-2">
                        <Avatar class="h-5 w-5">
                          {#if reply.author.avatar}
                            <AvatarImage src={reply.author.avatar} alt={reply.author.name} />
                          {/if}
                          <AvatarFallback>{reply.author.name[0]}</AvatarFallback>
                        </Avatar>
                        
                        <div class="flex-1">
                          <div class="flex items-center justify-between">
                            <span class="text-xs font-medium">{reply.author.name}</span>
                            <span class="text-xs text-muted-foreground">{formatTimestamp(reply.timestamp)}</span>
                          </div>
                          
                          <p class="text-xs mt-1 break-words">{reply.content}</p>
                        </div>
                      </div>
                    {/each}
                  </div>
                {/if}
              </div>
            </div>
          {/each}
        {:else}
          <div class="text-xs text-center text-muted-foreground py-4">
            暂无评论，快来发表第一条评论吧！
          </div>
        {/if}
      </div>
    </ScrollArea>
  </CardContent>
</Card>
