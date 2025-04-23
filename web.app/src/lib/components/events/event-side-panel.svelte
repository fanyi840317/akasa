<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import { fly, slide, fade } from "svelte/transition";
  import { cubicOut, cubicInOut } from "svelte/easing";
  import { crossfade } from "svelte/transition";
  import { ChevronLeft, ChevronDown, Settings } from "lucide-svelte";
  import { Button } from "$lib/components/ui/button";
  import { Badge } from "$lib/components/ui/badge";
  import type { Category } from "$lib/types/category";
  import type { Location } from "$lib/types/map";
  import type { Hypothesis, TimelineEvent } from "$lib/types/timeline";
  import EventPropertyCard from "./event-property-card.svelte";
  import EventTimelineCard from "./event-timeline-card.svelte";
  import EventCommentsCard from "./event-comments-card.svelte";

  import EventHypothesisStackedCard from "./event-hypothesis-stacked-card.svelte";

  // Define event types
  type EventTypes = {
    timelineChange: { timelineEvents: TimelineEvent[] };
    hypothesisChange: { hypotheses: Hypothesis[] };
    toggleSidebar: { isExpanded: boolean };
  };

  const dispatch = createEventDispatcher<EventTypes>();

  // 创建交叉淡入淡出动画
  const [send, receive] = crossfade({
    duration: 250,
    easing: cubicInOut,
  });

  // 当前激活的卡片
  let activeCard = $state<"property" | "timeline">("property"); // "property" 或 "timeline"

  // 鼠标悬停的卡片
  let hoverCard = $state<"property" | "timeline" | null>(null);

  // 侧边栏是否展开
  let isExpanded = $state(true);

  // 假说卡片是否可见
  let isHypothesisCardVisible = $state(true);

  // 切换侧边栏展开/收起状态
  function toggleSidebar() {
    isExpanded = !isExpanded;
    if (typeof onToggleSidebar === "function") {
      onToggleSidebar();
    }
  }

  // 切换激活的卡片
  function setActiveCard(card: "property" | "timeline"): void {
    activeCard = card;
  }

  // 设置鼠标悬停的卡片
  function setHoverCard(card: "property" | "timeline" | null): void {
    hoverCard = card;
  }

  // 计算卡片的变换样式
  function getCardTransform(card: string): string {
    if (activeCard === card) {
      return `translateY(0) scale(1) translateZ(0)`;
    } else if (hoverCard === card) {
      return `translateY(5px) scale(0.98) translateZ(0)`;
    } else {
      return `translateY(10px) scale(0.95) translateZ(0)`;
    }
  }

  // 计算卡片的不透明度
  function getCardOpacity(card: string): number {
    if (activeCard === card) {
      return 1;
    } else if (hoverCard === card) {
      return 0.9;
    } else {
      return 0.7;
    }
  }

  // 评论数据类型
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

  // 示例评论数据
  let comments = $state<Comment[]>([
    {
      id: "1",
      author: {
        name: "张三",
        avatar: "https://avatars.githubusercontent.com/u/93428946?v=4",
        role: "研究员",
      },
      content: "这个事件的时间线需要更多细节，我们应该添加更多的证据。",
      createdAt: new Date(2024, 5, 10),
    },
    {
      id: "2",
      author: {
        name: "李四",
        avatar: "https://avatars.githubusercontent.com/u/12345678?v=4",
        role: "分析师",
      },
      content: "我认为这个地点信息不太准确，需要重新核实。",
      createdAt: new Date(2024, 5, 12),
    },
    {
      id: "3",
      author: {
        name: "王五",
        avatar: "https://avatars.githubusercontent.com/u/87654321?v=4",
        role: "调查员",
      },
      content: "已经添加了新的证人证词，请查看最新的时间线。",
      createdAt: new Date(2024, 5, 15),
    },
  ]);

  let {
    eventDate = $bindable(undefined),
    locationData = $bindable(null),
    selectedCategories = $bindable([]),
    categories = [],
    timelineEvents = $bindable([]),
    hypotheses = $bindable([]),
    entitiesData = undefined,
    isLocation = $bindable(false),
    onToggleSidebar = () => {},
  } = $props<{
    eventDate?: string;
    locationData: Location | null;
    selectedCategories: string[];
    categories: Category[];
    timelineEvents: TimelineEvent[];
    hypotheses: Hypothesis[];
    entitiesData?: string;
    isLocation?: boolean;
    onToggleSidebar?: () => void;
  }>();

  // 如果提供了 entitiesData，则从中提取时间线数据
  $effect(() => {
    if (entitiesData) {
      try {
        // 检查 entitiesData 是否已经是对象
        let entities;
        if (typeof entitiesData === "object") {
          entities = entitiesData;
        } else if (entitiesData.startsWith("[") && entitiesData.endsWith("]")) {
          // 如果是数组格式的 JSON 字符串
          const entitiesArray = JSON.parse(entitiesData);
          entities = entitiesArray[0]; // 取第一个元素
        } else {
          // 尝试解析为 JSON 对象
          entities = JSON.parse(entitiesData);
        }

        if (entities && entities.timeline && Array.isArray(entities.timeline)) {
          // 将 entities.timeline 转换为 TimelineEvent 格式
          timelineEvents = entities.timeline.map(
            (item: any, index: number) => ({
              id: item.id || `timeline-${index}`,
              timestamp: new Date(item.time),
              description: item.event,
              evidenceIds: [],
              witnessIds: [],
            }),
          );
        }
      } catch (error) {
        console.error("解析 entities_data 失败:", error);
      }
    }
  });

  // 处理时间线变更
  function handleTimelineChange() {
    dispatch("timelineChange", {
      timelineEvents,
    } as EventTypes["timelineChange"]);
  }
</script>

<div
  class="flex flex-col w-[320px] px-3 rounded-l-lg relative h-[calc(100vh-120px)]"
>
  <!-- 收起按钮 -->
  <div class="absolute -right-4 top-1/2 transform -translate-y-1/2 z-50">
    <Button
      variant="outline"
      size="icon"
      class="h-8 w-8 rounded-full shadow-md bg-card hover:bg-card"
      onclick={toggleSidebar}
    >
      <ChevronLeft class="h-4 w-4" />
    </Button>
  </div>
  <!-- 卡片容器 -->
  <div class="relative w-full h-full flex flex-col">
    <!-- 卡片标签切换器 -->
    <div class="flex gap-2 px-4 mb-2 z-10 relative">
      <button
        class="text-xs font-medium px-3 py-1 rounded-md transition-all duration-200 flex items-center gap-1 relative"
        class:text-primary={activeCard === "property"}
        class:font-medium={activeCard === "property"}
        class:text-muted-foreground={activeCard !== "property"}
        class:hover:text-primary={activeCard !== "property"}
        onclick={() => setActiveCard("property")}
      >
        {#if activeCard === "property"}
          <div
            class="absolute inset-0 rounded-md bg-primary/5 border-[0.5px]
            border-primary/10 dark:bg-primary/10 dark:border-primary/20
            backdrop-filter backdrop-blur-[2px] shadow-sm"
            in:send={{ key: "activetab" }}
            out:receive={{ key: "activetab" }}
          ></div>
        {/if}
        <Settings class="h-3 w-3" />
        <span class="relative">属性</span>
      </button>

      <button
        class="text-xs font-medium px-3 py-1 rounded-md transition-all duration-200 flex items-center gap-1 relative"
        class:text-primary={activeCard === "timeline"}
        class:font-medium={activeCard === "timeline"}
        class:text-muted-foreground={activeCard !== "timeline"}
        class:hover:text-primary={activeCard !== "timeline"}
        onclick={() => setActiveCard("timeline")}
      >
        {#if activeCard === "timeline"}
          <div
            class="absolute inset-0 rounded-md bg-primary/5 border-[0.5px] border-primary/10 dark:bg-primary/10 dark:border-primary/20 backdrop-filter backdrop-blur-[2px] shadow-sm"
            in:send={{ key: "activetab" }}
            out:receive={{ key: "activetab" }}
          ></div>
        {/if}
        <span class="relative">时间线</span>
      </button>
    </div>

    <!-- 卡片叠加区域 -->
    <div class="relative w-full flex-1">
      <!-- 属性卡片 -->
      <div
        role="button"
        tabindex="0"
        class="absolute inset-0 transition-all duration-300 ease-out cursor-pointer"
        style:transform={getCardTransform("property")}
        style:z-index={activeCard === "property" ? "20" : "10"}
        style:opacity={getCardOpacity("property")}
        onmouseenter={() => setHoverCard("property")}
        onmouseleave={() => setHoverCard(null)}
        onclick={() => setActiveCard("property")}
        onkeydown={(e) => e.key === "Enter" && setActiveCard("property")}
      >
        <EventPropertyCard
          bind:eventDate
          bind:locationData
          bind:selectedCategories
          bind:isLocation
          {categories}
        />
      </div>

      <!-- 时间线卡片 -->
      <div
        role="button"
        tabindex="0"
        class="absolute inset-0 transition-all duration-300 ease-out cursor-pointer"
        style:transform={getCardTransform("timeline")}
        style:z-index={activeCard === "timeline" ? "20" : "10"}
        style:opacity={getCardOpacity("timeline")}
        onmouseenter={() => setHoverCard("timeline")}
        onmouseleave={() => setHoverCard(null)}
        onclick={() => setActiveCard("timeline")}
        onkeydown={(e) => e.key === "Enter" && setActiveCard("timeline")}
      >
        <EventTimelineCard
          bind:timelineEvents
          on:timelineChange={handleTimelineChange}
        />
      </div>
    </div>
  </div>

  <!-- 假说卡片 -->
  <EventHypothesisStackedCard
    bind:hypotheses
    on:hypothesisChange={(event: CustomEvent<{ hypotheses: Hypothesis[] }>) => {
      dispatch("hypothesisChange", { hypotheses: event.detail.hypotheses });
    }}
    on:toggleCard={() => (isHypothesisCardVisible = !isHypothesisCardVisible)}
  />

  <!-- 评论卡片 -->
  <EventCommentsCard {comments} />
</div>
