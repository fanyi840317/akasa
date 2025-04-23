<script lang="ts">
  import { fly } from "svelte/transition";
  import BorderBeam from "$lib/components/ui/grid-background/border-beam.svelte";

  // Define the comment type
  type Comment = {
    id: string;
    author: {
      name: string;
      avatar: string;
      role?: string;
    };
    content: string;
    createdAt: Date;
  };

  // Props
  let { comments = $bindable([]) } = $props<{
    comments: Comment[];
  }>();

  // Calculate the maximum number of avatars to show
  const MAX_AVATARS = 3;

  // Get the total number of comments
  let totalComments = $derived(comments.length);

  // Get the avatars to display (most recent first)
  let displayAvatars = $derived(comments
    .slice(0, MAX_AVATARS)
    .map((comment: Comment) => comment.author));
</script>

{#if comments.length > 0}
  <div
    class="mt-4 p-3 rounded-xl border border-gray-700/70 bg-neutral-900 relative"
    in:fly={{ y: 10, duration: 300 }}
  >
    <BorderBeam size={100} duration={10} />

    <div class="flex items-center justify-between">
      <div class="flex items-center">
        <!-- Overlapping avatars -->
        <div class="flex -space-x-3">
          {#each displayAvatars as author, i}
            <img
              src={author.avatar}
              alt={author.name}
              class="h-8 w-8 rounded-full ring-2 ring-background"
              style="z-index: {MAX_AVATARS - i};"
            />
          {/each}
        </div>

        <!-- Comment count -->
        <div class="ml-3 text-sm text-gray-400">
          {totalComments} 条评论
        </div>
      </div>

      <!-- View all button -->
      <button
        class="text-xs text-primary hover:text-primary/80 transition-colors"
        onclick={() => {/* Handle view all comments */}}
      >
        查看全部
      </button>
    </div>
  </div>
{/if}
