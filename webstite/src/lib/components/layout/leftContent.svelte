<script lang="ts">
  import { cn } from "$lib/utils";
  import { Motion } from "svelte-motion";
  import { CheckIcon, ChevronRightIcon, Search } from "lucide-svelte";
  import { onMount } from "svelte";
  import { cubicOut } from "svelte/easing";
  import { tweened } from "svelte/motion";
  import AnimatedSubscribeButton from "../ui/buttons/animatedSubscribeButton.svelte";
  import { UserAvatar } from "../ui/avatar";

  let { class: className = "", onExplore = () => {} } = $props();

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
  <!-- Main heading with animation -->
  <Motion
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.6 }}
    let:motion
  >
    <h1 use:motion class="text-4xl font-bold mb-4 tracking-wide antialiased">
      探索神秘 <br />
      未知的<span
        class=" px-2 py-1 shadow bg-base-300
     font-semibold text-5xl">世界</span
      >
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
    <p use:motion class="mb-6 text-sm tracking-wide">
      每一个神秘事件背后都有一个等待被讲述的故事, 探索未知，记录真相
    </p>
  </Motion>

  <!-- Search input with animation -->
  <Motion
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.6, delay: 0.3 }}
    let:motion
  ></Motion>

  <!-- Buttons with animation -->
  <Motion
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.6, delay: 0.4 }}
    let:motion
  >
    <div use:motion class="flex gap-4">
      <!-- <Button class="bg-purple-500 hover:bg-purple-600 text-white" onclick={handleSearch}>探索</Button> -->
      <AnimatedSubscribeButton text="探索" onclick={onExplore}
      ></AnimatedSubscribeButton>
    </div>
  </Motion>

  <!-- Event count with animation -->
  <Motion
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.6, delay: 0.6 }}
    let:motion
  >
    <div use:motion class="flex flex-col items-start mt-6 gap-2">
      <span class="text-sm tracking-wide">
        由 <span class="text-lg font-bold tracking-tight text-base-content"
          >{Math.round($animatedTotalContributors) || "..."}</span
        >
        位探索者分享了
        <span class="text-lg font-bold tracking-tight text-base-content"
          >{Math.round($animatedTotalEvents) || "..."}</span
        >
        个神秘事件
        <!-- <span class="ml-1">→</span> -->
      </span>
      {#if contributors.length > 0}
        <div class="avatar-group -space-x-2">
          {#each contributors.slice(0, 3) as contributor, i (contributor.id)}
            <UserAvatar
              class="w-12 h-12"
              src={contributor.avatarUrl}
              alt="Contributor Avatar"
              fallback={contributor.id.substring(0, 1).toUpperCase()}
            />
          {/each}
          <div class="avatar avatar-placeholder">
            <div
              class="bg-neutral text-neutral-content w-10 text-sm font-semibold"
            >
              <span>+99</span>
            </div>
          </div>
        </div>
      {/if}
    </div>
  </Motion>
</div>
