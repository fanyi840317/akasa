<script lang="ts">
  import { fly } from "svelte/transition";
  import { Sparkles } from "lucide-svelte";
  import type { Event } from "$lib/types/event";
  
  export let events: Event[] = [];
  export let onEventClick: (event: Event) => void = () => {};
  
  // 最多显示的事件数量
  const MAX_VISIBLE = 5;
  
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

<div class="fixed top-4 right-4 z-50 w-[280px] flex flex-col gap-2">
  <div class="text-base font-medium text-gray-800 dark:text-gray-200 mb-2 px-2">
    <span>身边的神秘事件</span>
  </div>
  
  <div class="overflow-hidden rounded-xl bg-white/10 dark:bg-black/10 backdrop-blur-md border border-gray-200/20 dark:border-gray-800/20 p-2">
    <div class="space-y-2">
      {#each events.slice(0, MAX_VISIBLE) as event, i}
        <button 
          type="button"
          in:fly={{ y: 10, delay: i * 100, duration: 300 }}
          class="w-full text-left bg-transparent border-none p-0 m-0 focus:outline-none focus-visible:ring-2 focus-visible:ring-primary/50 rounded-lg"
          on:click={() => onEventClick(event)}
          on:keydown={(e) => e.key === 'Enter' && onEventClick(event)}
        >
          <div class="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-100/20 dark:hover:bg-gray-900/20 transition-colors">
            <div class="relative w-16 h-16 rounded-lg overflow-hidden flex-shrink-0">
              <img 
                src={getCoverUrl(event)} 
                alt={event.title}
                class="w-full h-full object-cover"
              />
              <div class="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent"></div>
            </div>
            
            <div class="flex-1 min-w-0">
              <h3 class="text-sm font-medium text-gray-800 dark:text-gray-200 truncate">
                {event.title}
              </h3>
              
              <div class="flex gap-1 mt-1 flex-wrap">
                {#if event.tags && event.tags.length > 0}
                  {#each event.tags.slice(0, 1) as tag}
                    <span class="px-1.5 py-0.5 text-[10px] rounded-full bg-primary/10 text-primary text-xs">
                      {tag}
                    </span>
                  {/each}
                  {#if event.tags.length > 1}
                    <span class="px-1.5 py-0.5 text-[10px] rounded-full bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400">
                      +{event.tags.length - 1}
                    </span>
                  {/if}
                {/if}
              </div>
            </div>
          </div>
        </button>
      {/each}
    </div>
  </div>
</div>
