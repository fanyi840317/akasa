<script lang="ts">
  import type { PageData } from "./$types";
  import { Input } from "$lib/components/ui/input";
  import { Search } from "lucide-svelte";
  import EventCard from "$lib/components/ui/notion-cards/event-card.svelte";
  import TagNav from "$lib/components/ui/tag-nav/tag-nav.svelte";
  import { ScrollArea } from "$lib/components/ui/scroll-area/index.js";
  import { eventStore } from "$lib/stores/event";
  import { categoryStore } from "$lib/stores/category";
  import type { Event } from "$lib/types/event";
  import type { Category } from "$lib/types/category";
  import { fly } from "svelte/transition";
  import { onMount } from "svelte";
  import { ModeWatcher } from "mode-watcher";
  import { NotionPanel } from "$lib/components/layout";
  import EventView from "$lib/components/events/event-view.svelte";
  import { Motion } from "svelte-motion";
  import Globe from "$lib/components/ui/globe/Globe.svelte";
  import GlobeLeftContent from "$lib/components/ui/globe/GlobeLeftContent.svelte";
  import EventSidebarCards from "$lib/components/events/event-sidebar-cards.svelte";
  import EventStatsSidebar from "$lib/components/events/event-stats-sidebar.svelte";
  import { Sparkles } from "lucide-svelte";
  import BorderBeam from "$lib/components/ui/background/border-beam.svelte";
  import Marquee from "$lib/components/ui/marquee/Marquee.svelte";
  import Header from "$lib/components/website/header.svelte";
  import Footer from "$lib/components/website/footer.svelte";
  import DarkTiles from "$lib/components/ui/background/dark-tiles.svelte";
  import {
    Avatar,
    AvatarFallback,
    AvatarImage,
  } from "$lib/components/ui/avatar";
  import { cubicOut } from "svelte/easing";
  import { tweened } from "svelte/motion";
  import { cn } from "$lib/utils";
  import MapBase from "$lib/components/map/map-base.svelte";
  import { goto } from "$app/navigation";

  let events = $state<Event[]>([]);
  let categories = $state<Category[]>([]);
  let loading = $state(true);
  let selectedCategory = $state("all");

  // Panel 状态
  let showEventPanel = $state(false);
  let selectedEvent = $state<Event | null>(null);

  // 探索地图状态
  let showMap = $state(false);

  // Globe控制状态
  let targetCoordinates = $state<[number, number] | null>(null);
  let pauseMarquee = $state(false);

  // 搜索状态
  let searchQuery = $state("");

  // 处理探索按钮点击
  function handleExploreClick() {
    showMap = true;
    // 添加页面滚动到顶部，确保视图居中
    // window.scrollTo({ top: 0, behavior: 'smooth' });
    setTimeout(() => {
      goto("/events");
    }, 800);
  }

  // 处理返回按钮点击
  function handleReturnClick() {
    showMap = false;
    // 重置Globe状态
    targetCoordinates = null;
    pauseMarquee = false;
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

  // 分类标签

  // 处理搜索输入
  function handleSearchInput(e: any) {
    const target = e.target as HTMLInputElement;
    searchQuery = target.value;
  }

  // 过滤后的事件列表
  let filteredEvents = $state<Event[]>([]);

  // 更新过滤后的事件列表
  $effect(() => {
    // 先按类别筛选
    let filtered =
      selectedCategory === "all"
        ? events
        : events.filter(
            (event) =>
              event.categories && event.categories.includes(selectedCategory),
          );

    // 再按搜索关键词筛选
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(
        (event) =>
          event.title.toLowerCase().includes(query) ||
          event.content.toLowerCase().includes(query) ||
          (event.location_data?.city &&
            event.location_data.city.toLowerCase().includes(query)) ||
          (event.location_data?.country &&
            event.location_data.country.toLowerCase().includes(query)),
      );
    }

    filteredEvents = filtered;
  });

  // 获取事件和分类数据
  async function fetchData() {
    try {
      loading = true;
      const [eventsResponse, categoriesResponse] = await Promise.all([
        eventStore.fetchEvents(),
        categoryStore.fetchCategories(),
      ]);

      events = eventsResponse as unknown as Event[];
      categories = categoriesResponse;
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
  }

  // 处理面板关闭
  function handlePanelClose() {
    showEventPanel = false;
    selectedEvent = null;
  }
  let contributors: { id: string; avatarUrl: string }[] = $state([]);
  const tweenedOptions = { duration: 1000, easing: cubicOut };
  const animatedTotalEvents = tweened(0, tweenedOptions);
  const animatedTotalContributors = tweened(0, tweenedOptions);
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
        { id: "1", avatarUrl: "https://avatars.githubusercontent.com/u/1?v=4" },
        { id: "2", avatarUrl: "https://avatars.githubusercontent.com/u/2?v=4" },
        { id: "3", avatarUrl: "https://avatars.githubusercontent.com/u/3?v=4" },
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
          content: "在深山密林中发现的不明现象，多人目击光怪物体。",
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
        },
        {
          $id: "mock2",
          title: "海底异常信号",
          content: "深海探测器捕捉到的不明声波信号，可能来自未知生物。",
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
        },
        {
          $id: "mock3",
          title: "沙漠奇异光点",
          content: "沙漠中出现的不明光点，夜间移动并改变形状。",
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
        },
        {
          $id: "mock4",
          title: "古城府密室发现",
          content: "考古队在古城府遗址发现的密室，内有不明文字和图案。",
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

<ScrollArea class="">
  <Header />
  <!-- <div class=" p-4 rounded-lg text-white max-w-md pointer-events-auto">
      <Motion
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.6 }}
        let:motion
      >
        <div use:motion class="flex items-center">
          {#if contributors.length > 0}
            <div class="flex -space-x-2 mr-2">
              {#each contributors.slice(0, 3) as contributor (contributor.id)}
                <Avatar class="h-9 w-9 border border-neutral-300 bg-card">
                  <AvatarImage src={contributor.avatarUrl} alt="Contributor Avatar" />
                  <AvatarFallback>{contributor.id.substring(0, 1).toUpperCase()}</AvatarFallback>
                </Avatar>
              {/each}
            </div>
          {/if}
          <span class="text-sm text-gray-300">
            由 {Math.round($animatedTotalContributors) || '...'} 位探索者分享了 {Math.round($animatedTotalEvents) || '...'} 个神秘事件 <span class="ml-1">→</span>
          </span>
        </div>
      </Motion>
    </div> -->
  <div class="w-full h-[90vh] flex-1 flex flex-col relative bg-card">
    <div class=" flex flex-row items-center justify-center">
      <!-- 左侧：新增内容区域 -->
      <div class="w-2/5 h-full flex items-center justify-end pr-8">
        {#if !showMap}
          <div transition:fly={{ x: -200, duration: 800, delay: 0 }}>
            <GlobeLeftContent onExplore={handleExploreClick} />
          </div>
        {/if}
      </div>

      <!-- 中间：地球/地图组件 -->
      <div class="relative w-[300px] h-[300px] sm:w-[350px] sm:h-[350px] md:w-[400px] md:h-[400px] lg:w-[500px] lg:h-[500px] xl:w-[600px] xl:h-[600px]">
        <!-- 初始状态下的Globe组件 -->
        {#if !showMap}
          <div
            transition:fly={{ x: 200, duration: 800, delay: 0 }}
            class="w-full h-full flex items-center justify-center"
          >
            <Globe
              class="w-[300px] h-[300px] sm:w-[350px] sm:h-[350px] md:w-[400px] md:h-[400px] lg:w-[500px] lg:h-[500px] xl:w-[600px] xl:h-[600px] text-blue-500 dark:text-blue-400"
              {targetCoordinates}
              autoRotate={!pauseMarquee}
              color="green"
            />
          </div>
        {/if}
      </div>

      <!-- 右侧：事件跑马灯 -->
    </div>
    {#if !showMap}
      <div
        class="flex flex-row mt-10 mx-40 relative items-center justify-center"
        transition:fly={{ y: 100, duration: 600 }}
      >
        <Marquee pauseOnHover={pauseMarquee}>
          {#each events.slice(0, 4) as event}
            <article
              class="flex flex-row items-start justify-center relative gap-x-4 p-4 cursor-pointer transition-all hover:bg-black/5 dark:hover:bg-white/5 hover:scale-105 rounded-lg"
              transition:fly={{ y: 20, duration: 300 }}
              onmouseenter={() => handleEventHover(event)}
              onmouseleave={handleEventLeave}
            >
              <div class="flex flex-col items-center justify-center gap-y-1">
                <img
                  src={getCoverUrl(event)}
                  placeholder="blur"
                  alt="don corleone"
                  class="w-[120px] h-[80px] object-cover rounded-sm"
                />
                <!-- <div class="text-gray-300 z-10 text-xs">
                    {event.date.split("T")[0]}
                  </div> -->
              </div>

              <!-- <div
                        class="absolute inset-0 from-neutral-900/90 via-neutral-900/80 to-neutral-900/50
            rounded-xl bg-gradient-to-t backdrop-blur-[4px] transition-all duration-300"
                    ></div> -->

              <!-- <BorderBeam size={150} duration={12} /> -->
              <div
                class="flex flex-col flex-1 h-full items-start justify-center gap-y-1 mt-0.5"
              >
                <!-- <div class="flex items-center gap-x-4 text-xs">
                        <div class="text-gray-300 z-10">Mar 16, 2020</div>

                    </div> -->
                <h3
                  class=" text-md font-semibold leading-6
                      break-words line-clamp-1
                      text-gray-200 group-hover:text-gray-50"
                >
                  <a href="/">
                    {event.title.substring(0, 10)}
                  </a>
                </h3>
                <div class="text-gray-500 text-[10px]">
                  {event.date.split("T")[0]}
                </div>
                <div class="relative flex items-center gap-x-2">
                  <div class="text-[8px]">
                    <p class="text-white">
                      <a href="https://github.com/SikandarJODD">
                        <span class="absolute inset-0"></span>
                        {event.creator_name}
                      </a>
                    </p>
                    <!-- <p class="text-gray-500">Developer</p> -->
                  </div>
                  <img
                    src="https://avatars.githubusercontent.com/u/93428946?v=4"
                    alt="bhide"
                    class="h-4 w-4 rounded-full bg-gray-50"
                  />
                </div>
              </div>
            </article>
          {/each}
        </Marquee>
        <div
          class="pointer-events-none absolute inset-y-0 left-0 w-1/3 h-full bg-gradient-to-r from-white dark:from-card"
        ></div>
        <div
          class="pointer-events-none absolute inset-y-0 right-0 w-1/3 h-full bg-gradient-to-l from-white dark:from-card"
        ></div>
      </div>
    {/if}
  </div>

  <Footer />
</ScrollArea>

<style>
  /* 移除旧的网格样式 */
  :global(.bg-grid-white) {
    display: none;
  }
</style>
