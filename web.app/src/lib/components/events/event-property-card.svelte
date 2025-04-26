<script lang="ts">
  import { Card, CardContent } from "$lib/components/ui/card";
  import { cn } from "$lib/utils";
  import type { Category } from "$lib/types/category";
  import type { Location } from "$lib/types/map";
  import CategoryCard from "./property-cards/category-card.svelte";
  import DateCard from "./property-cards/date-card.svelte";
  import LocationCard from "./property-cards/location-card.svelte";

  let {
    eventDate = $bindable(undefined),
    locationData = $bindable(null),
    selectedCategories = $bindable([]),
    categories = [],
    isLocation = $bindable(false),
    className = "",
  } = $props<{
    eventDate?: string;
    locationData: Location | null;
    selectedCategories: string[];
    categories: Category[];
    isLocation?: boolean;
    className?: string;
  }>();

  // 导出 class
  export { className as class };

  // 卡片状态
  let activeCard = $state<"category" | "date" | "location">("category");
  let hoveredCard = $state<"category" | "date" | "location" | null>(null);

  // 卡片排序
  let cardOrder = $state<("category" | "date" | "location")[]>([
    "category",
    "date",
    "location",
  ]);

  // 获取卡片样式
  function getCardStyle(cardType: "category" | "date" | "location"): string {
    const isActive = activeCard === cardType;
    const isHovered = hoveredCard === cardType;

    // 获取卡片在排序中的位置
    const position = cardOrder.indexOf(cardType);

    // 设置基本参数
    let bottom = 0;
    let scale = 1;
    let zIndex = 30 - position; // 越靠前的卡片 z-index 越高
    // let opacity = 1 - position * 0.1; // 越靠后的卡片透明度越低
    let shadow = "";

    // 根据位置设置卡片的堆叠效果
    if (position === 0) {
      // 最上面的卡片
      bottom = 0;
      scale = 1;
      // shadow = "0px 25px 30px -3px rgba(0, 0, 0, 0.3)";
    } else {
      // 堆叠的卡片，每张卡片向下偏移 20px，并缩小 5%
      bottom = 30 * position;
      scale = 1 - position * 0.05;
      // shadow = `0px ${15 - position * 3}px ${20 - position * 4}px -2px rgba(0, 0, 0, ${0.25 - position * 0.05})`;
    }

    // 如果是悬停状态，向上移动并放大
    if (isHovered) {
      if (isActive) {
        // bottom -= 10;
      } else bottom += 30; // 向上移动 20px
    }

    return `bottom: ${bottom}px; transform: scale(${scale}); z-index: ${zIndex};`;
  }

  // 设置激活卡片
  function setActiveCard(cardType: "category" | "date" | "location") {
    // 如果点击当前激活卡片，不做任何操作
    if (activeCard === cardType) return;

    // 更新激活卡片
    activeCard = cardType;

    // 更新卡片排序，将激活卡片移动到最前面
    const newOrder = [...cardOrder];
    const index = newOrder.indexOf(cardType);
    if (index > -1) {
      newOrder.splice(index, 1); // 移除当前卡片
      newOrder.unshift(cardType); // 将当前卡片添加到最前面
      cardOrder = newOrder;
    }
  }

  // 设置悬停卡片
  function setHoveredCard(cardType: "category" | "date" | "location" | null) {
    hoveredCard = cardType;
  }
</script>

{#snippet PropertyStackedCard(type_str: "category" | "date" | "location")}
  <div
    role="button"
    tabindex="0"
    class="absolute w-full left-0 right-0 mx-auto transition-all duration-300 ease-out cursor-pointer"
    style={getCardStyle(type_str)}
    onmouseenter={() => setHoveredCard(type_str)}
    onmouseleave={() => setHoveredCard(null)}
    onclick={() => setActiveCard(type_str)}
    onkeydown={(e) => e.key === "Enter" && setActiveCard(type_str)}
  >
    <Card
      class={cn(
        "overflow-hidden transition-colors duration-300",
        activeCard === type_str
          ? " bg-white dark:bg-neutral-900 shadow-md"
          : hoveredCard === type_str
            ? "bg-muted border-border"
            : "bg-card border-border/70",
      )}
    >
      <CardContent class="h-[240px] overflow-hidden">
        {#if type_str === "category"}
          <CategoryCard bind:selectedCategories {categories} />
        {:else if type_str === "date"}
          <DateCard bind:eventDate />
        {:else if type_str === "location"}
          <LocationCard bind:locationData />
        {/if}
      </CardContent>
    </Card>
  </div>
{/snippet}

<div
  class={cn(
    "relative w-full h-[280px] mb-4 flex items-center justify-center",
    className,
  )}
>
  <!-- 分类卡片 -->
  {@render PropertyStackedCard("category")}

  <!-- 日期卡片 -->
  {@render PropertyStackedCard("date")}

  <!-- 位置卡片 -->
  {@render PropertyStackedCard("location")}
</div>
