<script lang="ts">
  import { fly } from "svelte/transition";
  import { ScrollArea } from "$lib/components/ui/scroll-area";
  import { Badge } from "$lib/components/ui/badge";
  import { Button } from "$lib/components/ui/button";
  import { Calendar, Clock, FileText, MapPin, Tag, X } from "lucide-svelte";
  import { backInOut } from "svelte/easing";
  import { Circle } from "lucide-svelte";

  export let event: {
    title: string;
    content: string;
    date: string;
    location?: string;
  };
  export let onClose: () => void;

  const keyFacts = [
    "1947年7月7日，新墨西哥州罗斯威尔附近发现不明飞行物残骸",
    "美国陆军空军基地最初发布声明称已捕获飞碟",
    "后来改口称是气象气球",
    "目击者描述看到金属碎片上有奇怪的符号",
    "多位证人称看到非人形生物尸体"
  ];

  const timeline = [
    { date: "1947-07-07", event: "牧场主布雷泽尔发现残骸" },
    { date: "1947-07-08", event: "军方发布捕获飞碟声明" },
    { date: "1947-07-09", event: "军方改口称是气象气球" },
    { date: "1978-12-", event: "首位目击者公开作证" },
    { date: "1994-09-", event: "美国空军发布最终报告" }
  ];
</script>

<div
  class="w-[400px] h-[80vh] bg-white dark:bg-neutral-900 border border-neutral-200/50 dark:border-neutral-800/50 shadow-[0_4px_12px_rgba(0,0,0,0.05)] dark:shadow-[0_4px_12px_rgba(0,0,0,0.2)] duration-300 rounded-xl overflow-hidden"
  in:fly={{ duration: 500, x: 100, delay: 200, easing: backInOut }}
  out:fly={{ duration: 400, x: 100, easing: cubicOut }}
>
  <ScrollArea class="h-full">
    <div class="p-6 flex flex-col gap-6">
      <!-- 标题区域 -->
      <div
        class="flex items-center justify-between"
        in:fly={{ duration: 300, y: -20, delay: 400 }}
      >
        <h2 class="text-xl font-semibold">{event.title}</h2>
        <Button
          variant="ghost"
          size="icon"
          class="h-8 w-8"
          onclick={onClose}
        >
          <X class="h-4 w-4" />
        </Button>
      </div>

      <!-- 关键信息 -->
      <div
        class="space-y-4"
        in:fly={{ duration: 300, y: -20, delay: 600 }}
      >
        <h3 class="text-sm font-medium text-neutral-500 dark:text-neutral-400">
          关键信息
        </h3>
        <div class="space-y-2">
          {#each keyFacts as fact}
            <div class="flex items-start gap-2">
              <div class="mt-1">
                <Circle class="h-2 w-2 text-neutral-400" />
              </div>
              <p class="text-sm">{fact}</p>
            </div>
          {/each}
        </div>
      </div>

      <!-- 时间线 -->
      <div
        class="space-y-4"
        in:fly={{ duration: 300, y: -20, delay: 800 }}
      >
        <h3 class="text-sm font-medium text-neutral-500 dark:text-neutral-400">
          时间线
        </h3>
        <div class="space-y-4">
          {#each timeline as item}
            <div class="flex gap-4">
              <div class="flex flex-col items-center">
                <div class="w-px h-3 bg-neutral-200 dark:bg-neutral-800" />
                <div
                  class="w-2 h-2 rounded-full bg-neutral-300 dark:bg-neutral-700"
                />
                <div class="flex-1 w-px bg-neutral-200 dark:bg-neutral-800" />
              </div>
              <div class="flex-1 pb-4">
                <p class="text-xs text-neutral-500 dark:text-neutral-400">
                  {item.date}
                </p>
                <p class="text-sm mt-1">{item.event}</p>
              </div>
            </div>
          {/each}
        </div>
      </div>

      <!-- 详细内容 -->
      <div
        class="space-y-4"
        in:fly={{ duration: 300, y: -20, delay: 1000 }}
      >
        <h3 class="text-sm font-medium text-neutral-500 dark:text-neutral-400">
          详细内容
        </h3>
        <p class="text-sm whitespace-pre-wrap">{event.content}</p>
      </div>
    </div>
  </ScrollArea>
</div> 