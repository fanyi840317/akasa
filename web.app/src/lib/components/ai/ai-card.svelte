<script lang="ts">
  import { Sparkles, RefreshCcw, ArrowRight, FileText } from "lucide-svelte";
  import { Button } from "$lib/components/ui/button";
  import { Card } from "$lib/components/ui/card";
  import { Badge } from "$lib/components/ui/badge";
  import { ScrollArea } from "$lib/components/ui/scroll-area";
  import Breadcrumb from "../ui/breadcrumb/breadcrumb.svelte";
  import { Separator } from "../ui/separator";
    import { onDestroy } from "svelte";

  export let position = { top: 0, left: 0 };
  export let minimized = false;
  export let onAction: (action: string, data?: any) => void = () => {};

  const examples = [
    {
      title: "深夜遇见的蓝光",
      content: `在2024年3月的一个深夜，我在回家的路上遇到了一个奇怪的现象。天空中出现了一个发着蓝光的不明物体，它静静地悬浮在空中大约10分钟...`,
      date: "2024-03-15",
    },
    {
      title: "古老钟声",
      content: `那是一个雨天的午后，我在一座废弃的教堂里避雨。突然间，教堂的钟楼传来了清脆的钟声，但是这座教堂的钟早已损坏多年...`,
      date: "2024-02-20",
    },
    {
      title: "消失的路人",
      content: `在一个雾气弥漫的清晨，我看到一个穿着复古服装的人从我面前走过，但当我转身想要看清时，那个人却完全消失了...`,
      date: "2024-01-10",
    },
  ];

  const recommendedEvents = [
    { id: 1, title: "凤凰城不明飞行物事件", date: "1997-03-13" },
    { id: 2, title: "百慕大三角神秘失踪案", date: "1945-12-05" },
    { id: 3, title: "尼斯湖水怪目击事件", date: "1934-04-21" },
    { id: 4, title: "罗斯威尔事件", date: "1947-07-08" },
    { id: 5, title: "通古斯大爆炸", date: "1908-06-30" },
    { id: 6, title: "贝尔岛灯塔事件", date: "1900-12-15" },
    { id: 7, title: "玛丽·赛勒斯特号失踪案", date: "1872-11-25" },
    { id: 8, title: "戴克洞穴之谜", date: "1925-08-14" },
    { id: 9, title: "费城实验", date: "1943-10-28" },
    { id: 10, title: "金字塔建造之谜", date: "前2560年" },
  ].slice(0, 10);

  function handleAction(action: string, data?: any) {
    onAction(action, data);
  }
  onDestroy(()=>{
      // alert();
    });
</script>



  {#if !minimized}
  <div
    class="fixed bg-white dark:bg-neutral-800 border border-neutral-200/50 dark:border-neutral-700/50 rounded-lg shadow-lg p-4 flex flex-col gap-4 z-50 ai-card w-[400px]"
    style="top: {position.top}px; left: {position.left+20}px;"
  >
    <!-- 亲身经历模式 -->
    <div class="space-y-2">
      <p class="text-xs text-muted-foreground/60 leading-relaxed">
        如果你有想分享的神秘经历，或者身边发生的离奇事件，你可以...
      </p>

      <ScrollArea class="h-[180px]">
        <div class="space-y-4">
          <div class="">
            <p class="text-lg font-medium mb-2 text-foreground">写作建议</p>
            <ul
              class="text-sm text-foreground/80 space-y-1 list-disc list-inside"
            >
              <li>发生的时间 & 地点</li>
              <li>事件具体经过</li>
              <li>你的感受 & 反应</li>
              <li>你对事件的猜测</li>
              <li>其他人的看法</li>
            </ul>
          </div>

          <div class="space-y-3">
            <p class="text-lg font-medium text-foreground">示例参考</p>
            {#each examples as example}
              <div class="space-y-1">
                <div class="flex items-center justify-between">
                  <p class="text-sm font-medium text-foreground/80">
                    {example.title}
                  </p>
                  <span class="text-[10px] text-foreground/60"
                    >{example.date}</span
                  >
                </div>
                <p class="text-xs text-foreground/60 leading-relaxed">
                  {example.content}
                </p>
              </div>
            {/each}
          </div>
        </div>
      </ScrollArea>

      <div class="flex gap-2 justify-between">
        <div class="flex items-center gap-2"></div>
        <Button
          variant="ghost"
          size="sm"
          class="text-muted-foreground/60 h-5 px-2"
          onclick={() =>
            handleAction("select-mode", {
              title: examples[0].title,
              content: `<h1>${examples[0].title}</h1>

<h2>发生时间</h2>
<p>${examples[0].date}</p>

<h2>发生地点</h2>
<p>[请补充具体地点]</p>

<h2>事件经过</h2>
<p>${examples[0].content}</p>

<h2>我的感受</h2>
<p>[描述当时的心情和想法]</p>

<h2>个人猜测</h2>
<p>[对这个事件的解释或推测]</p>

<h2>其他人的看法</h2>
<p>[周围人或目击者的反应和评论]</p>`,
            })}
        >
          <span class="text-xs font-medium">插入范本</span>
          <ArrowRight class="h-3.5 w-3.5 ml-1 text-muted-foreground/60" />
        </Button>
      </div>
    </div>

    <div class="relative">
      <div
        class="absolute inset-x-0 -ml-4 -mr-4 h-px bg-neutral-200 dark:bg-neutral-700"
      ></div>
    </div>

    <!-- 个人解读模式 -->
    <div class="space-y-3">
      <p class="text-xs text-muted-foreground/60 leading-relaxed">
        对已有事件有自己的看法和见解？选择一个感兴趣的事件...
      </p>

      <ScrollArea class="h-[120px]">
        <div class="flex flex-wrap gap-1.5 px-0.5 py-0.5">
          {#each recommendedEvents as event}
            <Badge
              variant="outline"
              class="flex items-center px-2 py-1 hover:bg-neutral-50 dark:hover:bg-neutral-900 transition-colors cursor-pointer font-normal border-neutral-200 dark:border-neutral-700 hover:border-neutral-300 dark:hover:border-neutral-600"
              onclick={() => handleAction("select-event", event)}
            >
              <span class="text-xs text-foreground/60 whitespace-nowrap"
                >{event.title}</span
              >
            </Badge>
          {/each}
        </div>
      </ScrollArea>

      <div class="flex gap-2 justify-between">
        <Button
          variant="ghost"
          size="sm"
          class="text-muted-foreground/40 h-5 w-5 p-0"
          onclick={() => handleAction("refresh-example")}
        >
          <RefreshCcw class="h-3.5 w-3.5" />
        </Button>
        <div class="flex-1 items-center gap-2"></div>
        <Button
          variant="ghost"
          size="sm"
          class="text-muted-foreground/60 h-5 px-2"
          onclick={() => handleAction("view-all-events")}
        >
          <span class="text-xs font-medium">查看所有事件</span>
        </Button>
        <Button
          variant="ghost"
          size="sm"
          class="text-muted-foreground/60 h-5 px-2"
          onclick={() => handleAction("view-all-events")}
        >
          <span class="text-xs font-medium">自己写</span>
        </Button>
      </div>
    </div>
  </div>
{/if}

<style>
  .ai-card {
    animation: cardEnter 150ms cubic-bezier(0.16, 1, 0.3, 1) forwards;
    transform-origin: top left;
  }

  @keyframes cardEnter {
    0% {
      opacity: 0;
      transform: scale(0.95);
    }
    100% {
      opacity: 1;
      transform: scale(1);
    }
  }
</style>
