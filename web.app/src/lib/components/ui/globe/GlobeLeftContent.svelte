<script lang="ts">
  import { cn } from "$lib/utils";
  import GridBeam from "$lib/components/ui/background/grid-beam.svelte";
  import { Button } from "$lib/components/ui/button";
  import { Motion } from "svelte-motion";
  import { Input } from "$lib/components/ui/input";
  import { CheckIcon, ChevronRightIcon, Search } from "lucide-svelte";
  import { eventStore } from "$lib/stores/event";
  import { onMount } from "svelte";
  import Avatar from "../avatar/avatar.svelte";
  import { AvatarFallback, AvatarImage } from "../avatar";
  import { cubicOut } from "svelte/easing";
  import { tweened } from "svelte/motion";
    import AnimatedSubscribeButton from "./AnimatedSubscribeButton.svelte";

  let {
    class: className = "",
    onExplore = () => {}
  } = $props();

  let searchQuery = "";
  const tweenedOptions = { duration: 1000, easing: cubicOut };
  const animatedTotalEvents = tweened(0, tweenedOptions);
  const animatedTotalContributors = tweened(0, tweenedOptions);
  let contributors: { id: string; avatarUrl: string }[] = $state([]); // 新增：存储贡献者列表

  // Fetch events count and contributors on mount
  onMount(async () => {
    try {
      // const events = await eventStore.fetchEvents();
      // totalEvents = events.length;

      // TODO: 替换为实际获取贡献者数据的逻辑
      // 示例：假设 eventStore 或其他服务提供 fetchContributors 方法
      // const fetchedContributors = await eventStore.fetchContributors({ limit: 3 });
      // totalContributors = fetchedContributors.totalCount;
      // contributors = fetchedContributors.data;

      // 暂时使用模拟数据
      animatedTotalEvents.set(902);

      animatedTotalContributors.set(123);
      contributors = [
        { id: "1", avatarUrl: "https://avatars.githubusercontent.com/u/1?v=4" },
        { id: "2", avatarUrl: "https://avatars.githubusercontent.com/u/2?v=4" },
        { id: "3", avatarUrl: "https://avatars.githubusercontent.com/u/3?v=4" },
      ];
    } catch (error) {
      console.error("Error fetching stats:", error);
    }
  });

  function handleSearch() {
    if (searchQuery.trim()) {
      // Navigate to search results page
      window.location.href = `/console/events?search=${encodeURIComponent(searchQuery)}`;
    }
  }
</script>

<div
  class={cn(
    "relative w-full h-full flex flex-col justify-center items-start",
    className,
  )}
>
  <!-- Background elements -->
  <GridBeam class="absolute inset-0 opacity-70">
    <div></div>
  </GridBeam>

  <!-- Content container with border beam effect -->
  <div class="relative z-10 max-w-md p-6">
    <!-- Main heading with animation -->
    <Motion
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      let:motion
    >
      <h1 use:motion class="text-5xl font-bold mb-4 text-white">
        探索神秘 <br />
        未知的<span class="bg-blue-800 px-2 py-1 border rounded font-semibold bg-gradient-to-b from-white to-neutral-700 text-transparent bg-clip-text">世界</span>

    </h1>
    </Motion>
    <!-- <span class="bg-blue-800 px-2 py-1 border rounded font-semibold bg-gradient-to-b from-white to-neutral-700 text-transparent bg-clip-text"><div>世界</div></span> -->
    <!-- Description text with animation -->
    <Motion
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: 0.2 }}
      let:motion
    >
      <p use:motion class="text-gray-400 mb-6 text-sm">
        每一个神秘事件背后都有一个等待被讲述的故事，探索未知，记录真相
      </p>
    </Motion>

    <!-- Search input with animation -->
    <Motion
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: 0.3 }}
      let:motion
    >
      <!-- <div use:motion class="relative mb-6">
        <Search class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <Input
          type="search"
          placeholder="搜索神秘事件..."
          class="pl-9 bg-black/30 border-gray-700 focus-visible:border-purple-500/50 focus-visible:ring-purple-500/30"
          bind:value={searchQuery}
          onkeypress={(e) => e.key === 'Enter' && handleSearch()}
        />
      </div> -->
    </Motion>

    <!-- Buttons with animation -->
    <Motion
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: 0.4 }}
      let:motion
    >
      <div use:motion class="flex gap-4">
        <!-- <Button class="bg-purple-500 hover:bg-purple-600 text-white" onclick={handleSearch}>探索</Button> -->
        <AnimatedSubscribeButton text="探索" onclick={onExplore}></AnimatedSubscribeButton>
      </div>
    </Motion>

    <!-- Event count with animation -->
    <Motion
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: 0.6 }}
      let:motion
    >
      <div use:motion class="flex items-center mt-6">
        {#if contributors.length > 0}
          <div class="flex justify-center relative">
            {#each contributors.slice(0, 3) as contributor, i (contributor.id)}
              <Avatar
                class="h-8 w-8 border border-white bg-gradient-to-br from-blue-400 to-purple-500"
                style="transform: translateX({i * -4}px); z-index: {3 -
                  i}; box-shadow: 0 2px 3px rgba(0, 0, 0, 0.1);"
              >
                <AvatarImage
                  src={contributor.avatarUrl}
                  alt="Contributor Avatar"
                />
                <AvatarFallback class="text-[10px]"
                  >{contributor.id
                    .substring(0, 1)
                    .toUpperCase()}</AvatarFallback
                >
              </Avatar>
            {/each}
          </div>
        {/if}
        <span class="text-sm text-gray-400">
          由 <span class="text-lg font-bold text-white tracking-tight"
            >{Math.round($animatedTotalContributors) || "..."}</span
          >
          位探索者分享了
          <span class="text-lg font-bold text-white tracking-tight"
            >{Math.round($animatedTotalEvents) || "..."}</span
          >
          个神秘事件
          <span class="ml-1">→</span>
        </span>
      </div>
    </Motion>
  </div>
</div>

<style>
  /* Add a subtle text shadow to the heading for better readability */
  h1 {
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  }
</style>
