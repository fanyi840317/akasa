<script lang="ts">
  import { fly } from "svelte/transition";
  import { Sparkles } from "lucide-svelte";
  import BorderBeam from "$lib/components/ui/background/border-beam.svelte";
  import type { Event } from "$lib/types/event";

  export let events: Event[] = [];
  export let onEventClick: (event: Event) => void = () => {};

  // 最多显示的事件数量
  const MAX_VISIBLE = 3;

  // 获取随机默认封面图
  function getRandomDefaultCover(): string {
    const defaultCovers = [
      "/images/cover/c1.webp",
      "/images/cover/c2.webp",
      "/images/cover/c3.webp",
    ];
    const randomIndex = Math.floor(Math.random() * defaultCovers.length);
    return defaultCovers[randomIndex];
  }

  // 处理封面图片
  function getCoverUrl(event: Event): string {
    if (!event.cover) return getRandomDefaultCover();

    try {
      // 检查是否是有效的 URL
      if (typeof event.cover === 'string') {
        if (event.cover.startsWith("http")) {
          return event.cover;
        } else {
          // 尝试解析 JSON 格式的封面数据
          const coverData = JSON.parse(event.cover);
          return coverData.url || getRandomDefaultCover();
        }
      }
      return getRandomDefaultCover();
    } catch (e) {
      return getRandomDefaultCover();
    }
  }
</script>

<div class="fixed top-4 right-4 z-50 flex flex-col gap-3 max-w-[280px]">
  <div class="text-xs text-gray-400 mb-1 px-2 flex items-center gap-1">
    <Sparkles class="h-3 w-3" />
    <span>身边的神秘事件</span>
  </div>
  {#each events.slice(0, MAX_VISIBLE) as event, i}
    <button
      type="button"
      in:fly={{ y: -20, delay: i * 100, duration: 300 }}
      class="w-full text-left bg-transparent border-none p-0 m-0 focus:outline-none focus-visible:ring-2 focus-visible:ring-purple-500/50 rounded-xl"
      on:click={() => onEventClick(event)}
      on:keydown={(e) => e.key === 'Enter' && onEventClick(event)}
    >
      <article class="relative rounded-2xl border border-gray-700/70 bg-black/60 backdrop-blur-sm overflow-hidden transition-all duration-300 hover:border-purple-500/50 hover:shadow-[0_0_15px_rgba(99,68,245,0.3)] hover:translate-y-[-4px] hover:scale-[1.02]">
        <BorderBeam size={80} duration={10} />
        <div class="p-4">
          <div class="relative w-full h-20 rounded-lg overflow-hidden mb-3">
            <img
              src={getCoverUrl(event)}
              alt={event.title}
              class="w-full h-full object-cover transition-transform duration-500 hover:scale-110"
            />
            <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
          </div>

          <h3 class="text-base font-medium text-gray-200 line-clamp-1 hover:text-purple-300 transition-colors">
            {event.title}
          </h3>

          <div class="flex gap-2 mt-2 flex-wrap">
            {#if event.tags && event.tags.length > 0}
              {#each event.tags.slice(0, 2) as tag}
                <span class="px-2 py-0.5 text-xs rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-300">
                  {tag}
                </span>
              {/each}
              {#if event.tags.length > 2}
                <span class="px-2 py-0.5 text-xs rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-300">
                  +{event.tags.length - 2}
                </span>
              {/if}
            {/if}
          </div>
        </div>
      </article>
    </button>
  {/each}
</div>
