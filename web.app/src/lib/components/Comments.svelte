
<script lang="ts">
  import { Avatar , AvatarImage, AvatarFallback} from "$lib/components/ui/avatar";
  import { Button } from "$lib/components/ui/button";
  import { ThumbsUp, MessageCircle, MoreVertical } from "lucide-svelte";
  import * as DropdownMenu from "$lib/components/ui/dropdown-menu";
  import { cn } from "$lib/utils";
  import type { Comment } from "$lib/types/comment";

  export let comments: Array<Comment & {
    isLiked?: boolean;
    user?: {
      name: string;
      avatar: string;
    };
  }>;

  export let onSubmit: (content: string) => void;

  let newComment = '';

  function handleSubmit() {
    if (newComment.trim()) {
      onSubmit(newComment);
      newComment = '';
    }
  }
</script>

<div class="space-y-6" id="comments-section">
  <h2 class="text-2xl font-semibold">评论</h2>

  <!-- 评论列表 -->
  <div class="space-y-6">
    {#each comments as comment (comment.id)}
      <div class="space-y-3">
        <div class="flex gap-4">
          <Avatar class="h-10 w-10">
            <AvatarImage src={comment.user?.avatar} alt={comment.user?.name} />
            <AvatarFallback>{comment.user?.name?.[0]}</AvatarFallback>
          </Avatar>

          <div class="flex-1 space-y-2">
            <div class="flex items-start justify-between">
              <div>
                <div class="flex items-center gap-2">
                  <span class="font-medium">{comment.user?.name}</span>
                  <span class="text-xs text-muted-foreground">
                    {new Date(comment.createdAt).toLocaleString()}
                  </span>
                </div>
                <p class="mt-2 text-sm text-muted-foreground">{comment.content}</p>
              </div>

              <!-- <DropdownMenu.Root>
                <DropdownMenu.Trigger asChild>
                  <Button variant="ghost" size="icon" class="h-8 w-8">
                    <MoreVertical class="h-4 w-4" />
                  </Button>
                </DropdownMenu.Trigger>
                <DropdownMenu.Content>
                  <DropdownMenu.Item>举报</DropdownMenu.Item>
                </DropdownMenu.Content>
              </DropdownMenu.Root> -->
            </div>

            <div class="flex items-center gap-4">
              <button
                class="flex items-center gap-1 text-sm text-muted-foreground hover:text-primary transition-colors"
                class:text-primary={comment.isLiked}
              >
                <ThumbsUp class="h-4 w-4" />
                <span>{comment.likes || 0}</span>
              </button>
              <button class="flex items-center gap-1 text-sm text-muted-foreground hover:text-primary transition-colors">
                <MessageCircle class="h-4 w-4" />
                <span>回复</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    {/each}
  </div>

  <!-- 评论输入框 -->
  <div class="flex gap-4">
    <Avatar class="h-10 w-10">
      <AvatarFallback>U</AvatarFallback>
    </Avatar>
    <div class="flex-1">
      <div class="rounded-lg border p-4">
        <textarea
          bind:value={newComment}
          class="min-h-[100px] w-full resize-none border-0 bg-transparent p-0 focus:outline-none focus:ring-0"
          placeholder="写下你的评论..."
        />
      </div>
      <div class="mt-4 flex justify-end">
        <Button on:click={handleSubmit}>发表评论</Button>
      </div>
    </div>
  </div>
</div>