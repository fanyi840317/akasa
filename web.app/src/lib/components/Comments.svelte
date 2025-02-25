
<script lang="ts">
  import { Avatar , AvatarImage, AvatarFallback} from "$lib/components/ui/avatar";
  import { Button } from "$lib/components/ui/button";
  import { ThumbsUp, MessageCircle, MoreVertical, ArrowUpDown } from "lucide-svelte";
  import * as DropdownMenu from "$lib/components/ui/dropdown-menu";
  import * as Pagination from "$lib/components/ui/pagination";
  import { cn } from "$lib/utils";
  import type { Comment } from "$lib/types/comment";
  import { mockComments } from "$lib/data/mock-comments";

  export let comments: Comment[];
  export let onSubmit: (content: string) => void;

  let newComment = '';
  let isInputFocused = false;
  let isDescending = true;

  // 分页相关状态
  let currentPage = 1;
  const pageSize = 10;
  $: totalPages = Math.ceil(comments.length / pageSize);
  $: paginatedComments = comments.slice((currentPage - 1) * pageSize, currentPage * pageSize);

  function handleSubmit() {
    if (newComment.trim()) {
      onSubmit(newComment);
      newComment = '';
      isInputFocused = false;
    }
  }

  function toggleOrder() {
    isDescending = !isDescending;
    comments = [...comments].reverse();
  }

  function handleFocus() {
    isInputFocused = true;
  }

  function handleBlur(event: FocusEvent) {
    const target = event.relatedTarget as HTMLElement;
    if (!target || !target.classList.contains('submit-button')) {
      isInputFocused = false;
    }
  }

  function goToPage(page: number) {
    if (page >= 1 && page <= totalPages) {
      currentPage = page;
    }
  }
</script>

<div class="space-y-6" id="comments-section">
  <div class="flex items-center justify-between">
    <div class="flex items-center gap-2">
      <h2 class="text-2xl font-semibold">评论</h2>
      <span class="text-sm text-muted-foreground">({comments.length})</span>
    </div>
    <Button variant="ghost" size="sm" class="gap-2" on:click={toggleOrder}>
      <ArrowUpDown class="h-4 w-4" />
      {isDescending ? '最新' : '最早'}
    </Button>
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
          class="w-full resize-none border-0 bg-transparent p-0 focus:outline-none focus:ring-0"
          placeholder="写下你的评论..."
          on:focus={handleFocus}
          on:blur={handleBlur}
        />
      </div>
      {#if isInputFocused || newComment}
        <div class="mt-4 flex justify-end">
          <Button on:click={handleSubmit} class="submit-button">发表评论</Button>
        </div>
      {/if}
    </div>
  </div>

  <!-- 评论列表 -->
  <div class="space-y-6">
    {#each paginatedComments as comment (comment.id)}
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

  <!-- 分页控制器 -->
  {#if totalPages > 0}
    <div class="mt-6">
      <Pagination.Root count={comments.length} perPage={pageSize}>
        {#snippet children({ pages, currentPage })}
          <Pagination.Content>
            <Pagination.Item>
              <Pagination.PrevButton />
            </Pagination.Item>
            {#each pages as page (page.key)}
              {#if page.type === "ellipsis"}
                <Pagination.Item>
                  <Pagination.Ellipsis />
                </Pagination.Item>
              {:else}
                <Pagination.Item isVisible={currentPage === page.value}>
                  <Pagination.Link {page} isActive={currentPage === page.value}>
                    {page.value}
                  </Pagination.Link>
                </Pagination.Item>
              {/if}
            {/each}
            <Pagination.Item>
              <Pagination.NextButton />
            </Pagination.Item>
          </Pagination.Content>
        {/snippet}
      </Pagination.Root>
    </div>
  {/if}
</div>