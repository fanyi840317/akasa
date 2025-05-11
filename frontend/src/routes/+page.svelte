<script lang="ts">
  import type { PageData } from "./$types";
  import { Search } from "lucide-svelte";

  import { fade, fly } from "svelte/transition";
  import { onMount } from "svelte";
  import { Motion } from "svelte-motion";
  import Globe from "$lib/components/ui/globe";
  import { Sparkles } from "lucide-svelte";

  import { cubicOut } from "svelte/easing";
  import { tweened } from "svelte/motion";
  import { cn } from "$lib/utils";
  import { goto } from "$app/navigation";
  import type { Event } from "$lib/types/event";
  import { eventStore } from "$lib/stores/event";
  import {  NotionPanel } from "$lib/components/layout";
  import { EventCardList, EventView } from "$lib/components/events";
  import { MapBase } from "$lib/components/map";

  let events = $state<Event[]>([]);
  let loading = $state(true);
  let selectedCategory = $state("all");

  // Panel 状态
  let showEventPanel = $state(false);
  let selectedEvent = $state<Event | null>(null);

  // 探索地图状态
  let showMap = $state(false);
  let mapBaseInstance: MapBase | null = $state(null); // Reference to MapBase instance

  // Globe控制状态
  let targetCoordinates = $state<[number, number] | null>(null);
  let pauseMarquee = $state(false);

  // 搜索状态
  let searchQuery = $state("");

  // 处理探索按钮点击
  async function handleExploreClick() {
    showMap = true;

    // Wait for the map component to potentially mount/render if needed
    // A small delay might be necessary in some Svelte reactivity scenarios
    await new Promise((resolve) => setTimeout(resolve, 50));

    if (navigator.geolocation && mapBaseInstance) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords;
          console.log(`Flying to user location: ${latitude}, ${longitude}`);
          mapBaseInstance?.flyTo(longitude, latitude, { zoom: 14 }); // Fly to user location with zoom
        },
        (error) => {
          console.error("Error getting user location:", error);
          // Optionally fly to a default location if geolocation fails
          // mapBaseInstance?.flyTo(DEFAULT_LNG, DEFAULT_LAT, { zoom: 1 });
        },
        {
          enableHighAccuracy: true,
          timeout: 5000,
          maximumAge: 0,
        },
      );
    } else {
      console.error(
        "Geolocation is not supported by this browser or map instance not ready.",
      );
      // Optionally fly to a default location
      // mapBaseInstance?.flyTo(DEFAULT_LNG, DEFAULT_LAT, { zoom: 1 });
    }
  }

  // 处理事件悬停
  function handleEventHover(event: Event) {
    if (event.location_data?.coordinates) {
      // 从location_data中提取坐标
      const { lat, lng } = event.location_data.coordinates;
      targetCoordinates = [lat, lng];
      pauseMarquee = true;
    }
  }

  // 处理事件离开悬停
  function handleEventLeave() {
    targetCoordinates = null;
    pauseMarquee = false;
  }

  // 过滤后的事件列表
  let filteredEvents = $state<Event[]>([]);

  // 获取事件和分类数据
  async function fetchData() {
    try {
      loading = true;
      const [eventsResponse] = await Promise.all([
        eventStore.fetchEvents(),
        //   categoryStore.fetchCategories(),
      ]);

      events = eventsResponse as unknown as Event[];
      // categories = categoriesResponse;
    } catch (error) {
      console.error("Failed to fetch data:", error);
    } finally {
      loading = false;
    }
  }

  // 处理卡片点击
  function handleEventClick(event: Event) {
    selectedEvent = event;
    showEventPanel = true;
    showMap = true;
    pauseMarquee = true; // 暂停轮播

    setTimeout(() => {
      // If the map is shown and the event has coordinates, fly to it
      if (mapBaseInstance && event.location_data?.coordinates) {
        const { lat, lng } = event.location_data.coordinates;
        console.log(`Flying to event location: ${lat}, ${lng}`);
        mapBaseInstance.flyTo(lng, lat, { zoom: 14 }); // Adjust zoom as needed

        // 设置目标坐标以在地球仪上显示
        if (!showMap) {
          targetCoordinates = [lat, lng];
        }
      }
    }, 50);
  }

  // 处理面板关闭
  function handlePanelClose() {
    showEventPanel = false;
    selectedEvent = null;
    pauseMarquee = false; // 恢复轮播
  }
  let contributors: { id: string; avatarUrl: string }[] = $state([]);
  const tweenedOptions = { duration: 1000, easing: cubicOut };
  const animatedTotalEvents = tweened(0, tweenedOptions);
  const animatedTotalContributors = tweened(0, tweenedOptions);
  // Note: The tweened function is deprecated but will be fixed in a separate update
  // 页面加载时获取数据
  onMount(() => {
    // 直接添加模拟数据以确保显示
    addMockEvents();

    // 然后尝试从服务器获取数据
    // fetchData();
    console.log("Fetching data...");
    // TODO: Replace with actual contributor fetching logic if needed
    // For now, using placeholder data similar to GlobeLeftContent
    // Fetch stats logic from GlobeLeftContent
    try {
      // const events = await eventStore.fetchEvents();
      animatedTotalEvents.set(events.length);

      animatedTotalContributors.set(123);
      contributors = [
        {
          id: "1",
          avatarUrl: "https://avatars.githubusercontent.com/u/1?v=4",
        },
        {
          id: "2",
          avatarUrl: "https://avatars.githubusercontent.com/u/2?v=4",
        },
        {
          id: "3",
          avatarUrl: "https://avatars.githubusercontent.com/u/3?v=4",
        },
      ];
    } catch (error) {
      console.error("Error fetching stats:", error);
    }
  });

  // 监听事件数据变化
  $effect(() => {
    console.log("Events loaded:", events.length);
    console.log("Filtered events:", filteredEvents.length);

    // 直接添加模拟数据以确保显示
    if (!loading && events.length === 0) {
      addMockEvents();
    }
  });

  // 添加模拟数据函数，确保有事件显示
  function addMockEvents() {
    if (events.length === 0) {
      console.log("Adding mock events...");
      const mockEvents = [
        {
          $id: "mock1",
          title: "神秘森林事件",
          content:
            "在深山密林中发现的不明现象，多人目击光怪物体。这是一段较长的描述性内容，用于测试多行文本的显示效果。",
          summary: "在深山密林中发现的不明现象，多人目击光怪物体。",
          cover: "https://images.unsplash.com/photo-1448375240586-882707db888b",
          tags: ["森林", "超自然"],
          categories: ["all"],
          date: new Date().toISOString(),
          user_id: "user1",
          creator_name: "探索者",
          creator_avatar:
            "https://api.dicebear.com/7.x/bottts/svg?seed=explorer",
          location_data: {
            coordinates: { lat: 39.9042, lng: 116.4074 },
            country: "CN",
            city: "北京",
          },
          views: 120,
          likes: 65,
        },
        {
          $id: "mock2",
          title: "海底异常信号",
          content: "深海探测器捕捉到的不明声波信号，可能来自未知生物。",
          summary: "深海探测器捕捉到不明声波信号。",
          cover: "https://images.unsplash.com/photo-1551244072-5d12893278ab",
          tags: ["海洋", "信号"],
          categories: ["all"],
          date: new Date().toISOString(),
          user_id: "user2",
          creator_name: "海洋学家",
          creator_avatar: "https://api.dicebear.com/7.x/bottts/svg?seed=ocean",
          location_data: {
            coordinates: { lat: 35.6762, lng: 139.6503 },
            country: "JP",
            city: "东京",
          },
          views: 250,
          likes: 180,
        },
        {
          $id: "mock3",
          title: "沙漠奇异光点",
          content: "沙漠中出现的不明光点，夜间移动并改变形状。",
          summary: "沙漠中出现不明光点，夜间移动并改变形状。",
          cover: "https://images.unsplash.com/photo-1509316785289-025f5b846b35",
          tags: ["沙漠", "光点"],
          categories: ["all"],
          date: new Date().toISOString(),
          user_id: "user3",
          creator_name: "沙漠向导",
          creator_avatar: "https://api.dicebear.com/7.x/bottts/svg?seed=desert",
          location_data: {
            coordinates: { lat: 29.9792, lng: 31.1342 },
            country: "EG",
            city: "开罗",
            name: "金字塔",
          },
          views: 90,
          likes: 40,
        },
        {
          $id: "mock4",
          title: "古城府密室发现",
          content: "考古队在古城府遗址发现的密室，内有不明文字和图案。",
          summary: "考古队在古城府遗址发现密室，内有不明文字图案。",
          cover: "https://images.unsplash.com/photo-1461988320302-91bde64fc8e4",
          tags: ["古迹", "密室"],
          categories: ["all"],
          date: new Date().toISOString(),
          user_id: "user4",
          creator_name: "考古学家",
          creator_avatar:
            "https://api.dicebear.com/7.x/bottts/svg?seed=ancient",
          location_data: {
            coordinates: { lat: 40.4319, lng: 116.5704 },
            country: "CN",
            city: "北京",
            name: "长城",
          },
          views: 300,
          likes: 220,
        },
        {
          $id: "mock5",
          title: "天空不明飞行物",
          content: "多人目击的天空不明飞行物，移动速度超过已知飞行器。",
          cover: "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a",
          tags: ["天空", "UFO"],
          categories: ["all"],
          date: new Date().toISOString(),
          user_id: "user5",
          creator_name: "天文爱好者",
          creator_avatar: "https://api.dicebear.com/7.x/bottts/svg?seed=sky",
          location_data: {
            coordinates: { lat: 37.7749, lng: -122.4194 },
            country: "US",
            city: "旧金山",
          },
        },
        {
          $id: "mock6",
          title: "山洞古老符文",
          content: "山洞中发现的不明符文，与已知文字系统不符。",
          cover: "https://images.unsplash.com/photo-1496275068113-fff8c90750d1",
          tags: ["山洞", "符文"],
          categories: ["all"],
          date: new Date().toISOString(),
          user_id: "user6",
          creator_name: "语言学家",
          creator_avatar: "https://api.dicebear.com/7.x/bottts/svg?seed=cave",
          location_data: {
            coordinates: { lat: 51.5074, lng: -0.1278 },
            country: "GB",
            city: "伦敦",
          },
        },
      ];

      events = [...mockEvents];
    }
  }
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

    return event.cover || getRandomDefaultCover();
  }
</script>

<div class="hero">
  <div class="hero-content flex-col lg:flex-row items-start">
    <div
      class="relative flex p-4 px-10"
      in:fly={{ x: -200, duration: 800, delay: 0 }}
      out:fly={{ x: -200, duration: 800, delay: 0 }}
    >
      <Globe color="" {targetCoordinates} autoRotate={!pauseMarquee} />
    </div>
    <div
      class="w-full"
      in:fly={{ x: 200, duration: 800, delay: 0 }}
      out:fly={{ x: 200, duration: 800, delay: 0 }}
    >
      <div class="flex items-center justify-between p-6">
        <div class="flex items-center justify-center gap-4">
          <span class="text-3xl font-bold">Events</span>
          <div class="badge badge-outline">2000条</div>
        </div>
      </div>
      <EventCardList
        {events}
        maxEvents={4}
        onEventHover={handleEventHover}
        onEventLeave={handleEventLeave}
        onEventClick={handleEventClick}
        {getCoverUrl}
      />
    </div>
  </div>
</div>

<!-- <div class="flex size-full items-center justify-center" transition:fly={{ y: 100, duration: 600 }}>
   
</div> -->

<!-- {#if !showMap}{:else}
    <div
        class="absolute w-full h-[100vh] inset-0 flex items-start justify-end"
        in:fade={{ duration: 1200, delay: 200 }}
        out:fade={{ duration: 1200, delay: 200 }}
    >
        <MapBase
            class="w-1/3 h-[full] map-with-mask"
            zoom={12}
            showUserLocation={true}
        />
    </div>
{/if} -->

<!-- 事件详情面板 -->

<style>
  :global(.map-with-mask) {
    mask-image: radial-gradient(circle at center, black 10%, transparent 80%);
    -webkit-mask-image: radial-gradient(
      circle at center,
      black 10%,
      transparent 80%
    );
  }
</style>
