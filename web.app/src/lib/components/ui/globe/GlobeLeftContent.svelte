<script lang="ts">
  import { cn } from "$lib/utils";
  import GridBeam from "$lib/components/ui/background/grid-beam.svelte";
  import { Button } from "$lib/components/ui/button";
  import { Motion } from "svelte-motion";
  import { Input } from "$lib/components/ui/input";
  import { Search } from "lucide-svelte";
  import { eventStore } from "$lib/stores/event";
  import { onMount } from "svelte";
    import Avatar from "../avatar/avatar.svelte";
    import { AvatarFallback, AvatarImage } from "../avatar";

  let className = '';
  export { className as class };

  let searchQuery = '';
  let totalEvents = 0;

  // Fetch events count on mount
  onMount(async () => {
    try {
      const events = await eventStore.fetchEvents();
      totalEvents = events.length;
    } catch (error) {
      console.error("Error fetching events:", error);
    }
  });

  function handleSearch() {
    if (searchQuery.trim()) {
      // Navigate to search results page
      window.location.href = `/console/events?search=${encodeURIComponent(searchQuery)}`;
    }
  }
</script>

<div class={cn("relative w-full h-full flex flex-col justify-center items-start", className)}>
  <!-- Background elements -->
  <GridBeam class="absolute inset-0 opacity-70" >
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
        未知的 <span class="bg-blue-800 px-2 py-1 rounded">世界</span>
      </h1>
    </Motion>

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
      <div use:motion class="relative mb-6">
        <Search class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <Input
          type="search"
          placeholder="搜索神秘事件..."
          class="pl-9 bg-black/30 border-gray-700 focus-visible:border-purple-500/50 focus-visible:ring-purple-500/30"
          bind:value={searchQuery}
          onkeypress={(e) => e.key === 'Enter' && handleSearch()}
        />
      </div>
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
        <Button variant="ghost" class="text-white hover:bg-gray-800/30" onclick={() => window.location.href = '/console/events/create'}>
          <span class="mr-2 text-xs">+</span> 创建事件
        </Button>
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
        <div class="flex -space-x-2">
          <Avatar class="h-6 w-6 border-2 border-background">
            <AvatarImage src="https://api.dicebear.com/7.x/bottts/svg?seed=explore" alt="User Avatar" />
            <AvatarFallback>U</AvatarFallback>

          </Avatar>
          <Avatar class="h-6 w-6 border-2 border-background">
            <AvatarImage src="https://api.dicebear.com/7.x/bottts/svg?seed=explore" alt="User Avatar" />
            <AvatarFallback>U</AvatarFallback>

          </Avatar>
       </div>
        <span class="ml-2 text-sm text-gray-400">已收录 {totalEvents || '...'} 个神秘事件 <span class="ml-1">→</span></span>
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
