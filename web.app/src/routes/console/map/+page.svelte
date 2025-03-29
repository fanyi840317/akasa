<script lang="ts">
  import type { PageData } from "./$types";
  import { Button } from "$lib/components/ui/button";
  import type { ShellContext } from "../../../lib/types/types";
  import { _ } from "svelte-i18n";
  import { Search, MapPin, PlusCircle, Users, Bell, Settings } from "lucide-svelte";
  import {MapBase as Map} from "$lib/components/ui/map";
  import EventList from "./event-list.svelte";
  import TagNav from "$lib/components/ui/tag-nav/tag-nav.svelte";
  import { getContext, onMount, setContext } from "svelte";
  import { writable } from "svelte/store";
  import { goto } from "$app/navigation";
  import { categoryStore } from "$lib/stores/category";
  import { eventStore } from "$lib/stores/event";
  import type { Category } from "$lib/types/category";
  import type { Event } from "$lib/types/event";
  import { mapStore } from '$lib/stores/map';

  let { data }: { data: PageData } = $props();

  interface CategoryResponse {
    $id: string;
    name: {
      zh: string;
      [key: string]: string;
    };
    color: string;
  }

  // 修复分类数据的类型
  interface CategoryItem {
    id: string;
    name: string;
    color: string;
  }

  // 选中的事件数据
  let selectedEvent = $state<Event | null>(null);

  // 分类标签
  let categoryItems = $state<CategoryItem[]>([
    { id: "all", name: "全部", color: "#94a3b8" }
  ]);

  // 事件列表数据
  let events = $state<Event[]>([]);
  let filteredEvents = $state<Event[]>([]);

  let selectedCategory = $state("all");
  let searchQuery = "";
  let currentPage = 1;
  const itemsPerPage = 6;
  let totalPages = 1;

  // 添加状态变量
  let eventTitle = $state("");
  let eventDescription = $state("");
  let eventLocation = $state("");
  let eventDate = $state("");
  let showCreatePanel = $state(false);

  // 模拟数据
  const mockEvents: Event[] = [
    {
      $id: "1",
      $createdAt: new Date().toISOString(),
      $updatedAt: new Date().toISOString(),
      title: "神秘的地下隧道",
      content: "在市中心发现一条未知的地下隧道，墙壁上刻有奇怪的符号...",
      location: "北京市朝阳区",
      date: new Date().toISOString(),
      user_id: "user1",
      is_public: true,
      cover_image: "/images/cover/c1.webp",
      status: "unverified",
      category: "mysterious",
      creator_name: "探险者",
      creator_avatar: "/images/avatars/avatar1.png",
      latitude: 39.9242,
      longitude: 116.4174
    },
    {
      $id: "2",
      $createdAt: new Date().toISOString(),
      $updatedAt: new Date().toISOString(),
      title: "消失的街道",
      content: "一条街道在深夜突然消失，第二天早上又出现...",
      location: "北京市东城区",
      date: new Date().toISOString(),
      user_id: "user2",
      is_public: true,
      cover_image: "/images/cover/c2.webp",
      status: "unverified",
      category: "paranormal",
      creator_name: "都市传说",
      creator_avatar: "/images/avatars/avatar2.png",
      latitude: 39.9142,
      longitude: 116.4074
    },
    {
      $id: "3",
      $createdAt: new Date().toISOString(),
      $updatedAt: new Date().toISOString(),
      title: "时间异常区域",
      content: "某区域的时间流速异常，手表显示时间比实际时间快/慢...",
      location: "北京市西城区",
      date: new Date().toISOString(),
      user_id: "user3",
      is_public: true,
      cover_image: "/images/cover/c3.webp",
      status: "unverified",
      category: "supernatural",
      creator_name: "时间观察者",
      creator_avatar: "/images/avatars/avatar3.png",
      latitude: 39.9342,
      longitude: 116.3974
    }
  ];

  // 地图相关状态
  let mapInstance: any = null;
  let markers: any[] = [];
  let hoveredMarker: any = null;

  // 定义事件分类和对应的颜色
  const EVENT_CATEGORIES = {
    EMERGENCY: { name: '紧急', color: '#FF4D4F' },
    WARNING: { name: '警告', color: '#FAAD14' },
    NOTICE: { name: '提示', color: '#1890FF' },
    INFO: { name: '信息', color: '#52C41A' },
    SPECIAL: { name: '特殊', color: '#722ED1' }
  };

  // 获取随机分类
  function getRandomCategory() {
    const categories = Object.keys(EVENT_CATEGORIES);
    const randomIndex = Math.floor(Math.random() * categories.length);
    return {
      type: categories[randomIndex],
      ...EVENT_CATEGORIES[categories[randomIndex]]
    };
  }

  // 页面加载时获取数据
  onMount(() => {
    fetchEvents();
    fetchCategories();
  });

  // 获取分类数据
  async function fetchCategories() {
    try {
      const categories = await categoryStore.fetchCategories() as CategoryResponse[];
      if (Array.isArray(categories)) {
        categoryItems = [
          { id: "all", name: "全部", color: "#94a3b8" },
          ...categories.map(cat => ({
            id: cat.$id,
            name: cat.name?.zh || '未命名',
            color: cat.color || '#94a3b8'
          }))
        ];
      }
    } catch (error) {
      console.error('Failed to fetch categories:', error);
    }
  }

  // 获取事件数据
  async function fetchEvents() {
    try {
      const fetchedEvents = await eventStore.fetchEvents();
      if (fetchedEvents && fetchedEvents.length > 0) {
        // 直接为所有事件添加坐标和随机分类
        events = fetchedEvents.map(event => {
          // 使用更复杂的哈希算法
          const hash = event.$id.split('').reduce((acc, char, index) => {
            return acc + (char.charCodeAt(0) * (index + 1));
          }, 0);
          
          // 生成更随机的坐标
          const latOffset = (hash % 20 - 10) * 0.01; // -0.1 到 0.1 的范围
          const lngOffset = ((hash >> 8) % 20 - 10) * 0.01; // 使用不同的位来生成经度偏移
          
          const lat = 39.9042 + latOffset;
          const lng = 116.4074 + lngOffset;

          // 添加随机分类
          const category = getRandomCategory();
          
          return {
            ...event,
            latitude: lat,
            longitude: lng,
            category: category.type,
            categoryName: category.name,
            color: category.color
          };
        });
      } else {
        console.log('No events fetched, using mock data');
        events = mockEvents.map(event => {
          const category = getRandomCategory();
          return {
            ...event,
            category: category.type,
            categoryName: category.name,
            color: category.color
          };
        });
      }
      filterEvents();
    } catch (error) {
      console.error('Failed to fetch events:', error);
      console.log('Using mock data due to fetch error');
      events = mockEvents.map(event => {
        const category = getRandomCategory();
        return {
          ...event,
          category: category.type,
          categoryName: category.name,
          color: category.color
        };
      });
      filterEvents();
    }
  }

  // 过滤事件
  function filterEvents() {
    let filtered = [...events];
    if (selectedCategory !== "all") {
      filtered = filtered.filter(event => event?.category === selectedCategory);
    }
    filteredEvents = filtered;
    totalPages = Math.ceil(filteredEvents.length / itemsPerPage);
    
    // 添加日志
    console.log('Filtered events:', filteredEvents);
    console.log('Events with coordinates:', filteredEvents.filter(e => e.latitude && e.longitude));
  }

  // 监听分类变化
  // $effect(() => {
  //   filterEvents();
  // });

  function handleCategoryClick(categoryId: string) {
    selectedCategory = categoryId;
    filterEvents();
  }

  function handleEventClick(event: Event) {
    selectedEvent = event;
    if (event.$id) {
      goto(`/console/events/${event.$id}`);
    }
  }

  function formatDate(dateString: string) {
    const date = new Date(dateString);
    return date.toLocaleDateString("zh-CN", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  }

  function getStaggerDelay(i: number) {
    return i * 50;
  }

  function getCategoryTransform(index: number, total: number) {
    const verticalSpacing = 60;
    return `translate(0, ${index * verticalSpacing}px)`;
  }

  function handleCreateEvent() {
    eventTitle = "";
    eventDescription = "";
    eventLocation = "";
    eventDate = "";
    showCreatePanel = true;
  }

  function handleClosePanel() {
    showCreatePanel = false;
  }

  function handleMapLoad(event: CustomEvent) {
    console.log('Map loaded event received:', event);
    mapInstance = event.detail.map;
    
    // 验证地图中心点
    if (mapInstance) {
      const center = mapInstance.getCenter();
      console.log('Map center after load:', center);
      
      // 确保地图中心点正确
      if (center.lng !== 116.4074 || center.lat !== 39.9042) {
        console.log('Setting correct center point');
        mapInstance.setCenter([116.4074, 39.9042]);
      }
    }

    if (mapInstance && events.length > 0) {
      console.log('Adding markers for events:', events);
      addMarkersToMap();
    }
  }

  function handleLocationClick() {
    console.log('Location button clicked');
    if ("geolocation" in navigator) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          console.log('Got position:', position);
          const { latitude, longitude } = position.coords;
          if (mapInstance) {
            console.log('Setting map location:', { latitude, longitude });
            mapInstance.setLocation(longitude, latitude);
            mapInstance.setZoom(15);
          } else {
            console.error('Map instance not available');
          }
        },
        (error) => {
          console.error("Error getting location:", error);
        }
      );
    } else {
      console.error("Geolocation is not supported by this browser.");
    }
  }

  function getCategoryCount(categoryId: string): number {
    return filteredEvents.filter(e => e?.category === categoryId).length;
  }

  // 添加标记到地图
  function addMarkersToMap() {
    console.log('Starting to add markers for events:', events);

    // 清除现有标记
    mapStore.removeAllMarkers();

    // 添加新标记
    events.forEach(event => {
      if (event.latitude && event.longitude) {
        console.log('Adding marker for event:', {
          title: event.title,
          position: [event.longitude, event.latitude],
          category: event.category
        });

        mapStore.addMarker({
          position: [event.longitude, event.latitude],
          color: getCategoryColor(event.category),
          size: 16, // 增大标记点大小
          className: 'event-marker',
          data: event
        });
      } else {
        console.warn('Event missing coordinates:', event.title);
      }
    });
  }

  // 获取分类颜色
  function getCategoryColor(category: string | undefined): string {
    const categoryItem = categoryItems.find(c => c.id === category);
    const color = categoryItem?.color || '#94a3b8';
    console.log('Category color for', category, ':', color);
    return color;
  }

  // 显示事件预览
  function showEventPreview(event: Event) {
    const preview = document.createElement('div');
    preview.className = 'event-preview';
    preview.innerHTML = `
      <div class="preview-content">
        <h3>${event.title}</h3>
        <p>${event.location}</p>
      </div>
    `;
    document.body.appendChild(preview);
  }

  // 隐藏事件预览
  function hideEventPreview() {
    const preview = document.querySelector('.event-preview');
    if (preview) {
      preview.remove();
    }
  }

  // 监听事件数据变化
  $effect(() => {
    if (events.length > 0) {
      console.log('Events changed, updating markers');
      addMarkersToMap();
    }
  });

  // 更新地图标记
  function updateMapMarkers() {
    if (!mapInstance) return;
    
    const markers = filteredEvents.map(event => ({
      position: [event.longitude, event.latitude],
      color: event.color,
      category: event.categoryName,
      className: 'event-marker',
      data: {
        title: event.title,
        location: event.location
      }
    }));

    mapStore.set(markers);
  }
</script>

<div class="w-full h-screen flex flex-col relative">
  <!-- 地图容器 -->
  <div class="absolute inset-0 z-0">
    <Map 
      on:mapLoad={handleMapLoad}
      locationData={{ 
        latitude: 39.9042, 
        longitude: 116.4074
      }}
      zoom={12}
      showUserLocation={true}
    />
  </div>

  <!-- 黑雾蒙层 -->
  <div
    class="absolute inset-0 z-10 pointer-events-none"
    style="background: radial-gradient(circle at center, transparent 30%, hsl(var(--background) / 0.2) 50%, hsl(var(--background) / 0.9) 100%)"
  ></div>

  <!-- 顶部标题和按钮区域 -->
  <div class="relative z-20">
    <!-- 内容区域 -->
    <div class="container mx-auto pt-24 pb-8 space-y-16">
      <!-- 标题区域 -->
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
        <div class="space-y-2">
          <div class="flex items-center gap-4">
            <h1 class="text-4xl font-bold bg-gradient-to-r from-primary via-primary to-primary/90 bg-clip-text text-transparent drop-shadow-[0_0_15px_rgba(var(--primary),0.3)]">
              {$_("site.events")}
            </h1>
            <div class="flex items-center gap-2 text-sm text-white/80">
              <div class="flex items-center gap-1.5">
                <div class="h-2 w-2 rounded-full bg-green-500 animate-pulse shadow-[0_0_10px_rgba(34,197,94,0.5)]"></div>
                <span>在线</span>
              </div>
              <div class="flex items-center gap-1.5">
                <Users class="h-4 w-4" />
                <span>128 探索者</span>
              </div>
            </div>
          </div>
          <h2 class="text-sm text-white/80 font-medium">{$_("events.subtitle")}</h2>
        </div>
        <div class="flex items-center gap-3">
          <button class="nav-button">
            <Bell class="h-5 w-5" />
          </button>
          <button class="nav-button">
            <Settings class="h-5 w-5" />
          </button>
          <Button variant="ghost" size="icon" class="h-10 w-10 rounded-full bg-white/5 hover:bg-white/10">
            <Search class="h-5 w-5" />
          </Button>
          <Button 
            variant="ghost" 
            size="icon" 
            class="h-10 w-10 rounded-full bg-white/5 hover:bg-white/10"
            onclick={() => handleLocationClick()}
          >
            <MapPin class="h-5 w-5" />
          </Button>
        </div>
      </div>

      <!-- 分类标签 -->
      <div class="flex flex-wrap gap-3">
        {#each categoryItems as category}
          <button
            class="category-tag"
            class:selected="{selectedCategory === category.id}"
            style="--tag-color: {category.color}"
            on:click={() => handleCategoryClick(category.id)}
          >
            <div class="category-dot"></div>
            <span class="category-name">{category.name}</span>
            {#if category.id !== 'all'}
              <div class="category-count">
                {filteredEvents.filter(e => e.category === category.id).length}
              </div>
            {/if}
          </button>
        {/each}
      </div>
    </div>
  </div>

  <!-- 底部事件展示区域 -->
  <div class="relative mt-auto mx-auto max-w-[1200px] px-14 mb-6">
    <EventList events={filteredEvents} cardclick={handleEventClick} />
  </div>
</div>

<style lang="postcss">
  :global(.dark) {
    color-scheme: dark;
  }

  .category-tag {
    @apply px-4 py-2 rounded-full transition-all duration-200 flex items-center gap-2;
    @apply bg-white/5 backdrop-blur-md shadow-lg;
    @apply hover:bg-white/10;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 
                0 2px 4px -1px rgba(0, 0, 0, 0.06),
                inset 0 0 0 1px rgba(255, 255, 255, 0.1);
  }

  .category-tag.selected {
    @apply bg-white/15 text-white;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 
                0 2px 4px -1px rgba(0, 0, 0, 0.06),
                inset 0 0 0 1px rgba(255, 255, 255, 0.2),
                0 0 0 2px var(--tag-color);
  }

  .category-dot {
    @apply w-2 h-2 rounded-full transition-all duration-200;
    background-color: var(--tag-color);
    box-shadow: 0 0 10px var(--tag-color);
  }

  .selected .category-dot {
    @apply opacity-100;
    transform: scale(1.2);
  }

  :not(.selected) .category-dot {
    @apply opacity-70;
  }

  .category-name {
    @apply text-sm font-medium;
  }

  .category-count {
    @apply px-2 py-0.5 rounded-full bg-black/20 backdrop-blur-md text-xs;
  }

  .nav-button {
    @apply p-2 rounded-lg;
    @apply bg-white/5 backdrop-blur-md;
    @apply text-white/80 hover:text-white;
    @apply transition-all duration-300;
    @apply hover:bg-white/10;
    @apply border border-white/5;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1),
                0 2px 4px -1px rgba(0, 0, 0, 0.06);
  }

  .title-section {
    @apply relative;
    @apply bg-gradient-to-b from-white/5 to-transparent;
    @apply rounded-3xl;
    @apply p-8;
    @apply border border-white/10;
    box-shadow: 0 8px 32px -4px rgba(0, 0, 0, 0.2),
                0 4px 16px -2px rgba(0, 0, 0, 0.1),
                inset 0 0 0 1px rgba(255, 255, 255, 0.1);
  }

  .title-section::before {
    content: '';
    @apply absolute inset-0 rounded-3xl;
    background: radial-gradient(circle at top left, rgba(var(--primary), 0.1), transparent 50%);
    pointer-events: none;
  }

  .title-content {
    @apply flex flex-col md:flex-row justify-between items-start md:items-center gap-6;
  }

  .title-left {
    @apply space-y-4;
  }

  .title-wrapper {
    @apply space-y-2;
  }

  .main-title {
    @apply relative text-4xl font-bold;
    @apply bg-gradient-to-r from-primary via-primary to-primary/90;
    @apply bg-clip-text text-transparent;
    text-shadow: 0 0 15px rgba(var(--primary), 0.3);
  }

  .title-glow {
    @apply absolute inset-0;
    @apply bg-primary/20 blur-2xl;
    @apply -z-10;
    @apply rounded-full;
    @apply animate-pulse;
  }

  .subtitle {
    @apply text-sm text-white/60 font-medium;
  }

  .status-badges {
    @apply flex items-center gap-4;
  }

  .status-badge {
    @apply flex items-center gap-2;
    @apply px-3 py-1.5 rounded-full;
    @apply bg-white/5 backdrop-blur-md;
    @apply text-sm text-white/60;
    @apply border border-white/5;
  }

  .status-dot {
    @apply w-2 h-2 rounded-full bg-green-500;
    @apply animate-pulse;
  }

  .action-buttons {
    @apply flex items-center gap-3;
  }

  .action-button {
    @apply p-2 rounded-lg;
    @apply bg-white/5 backdrop-blur-md;
    @apply text-white/80 hover:text-white;
    @apply transition-all duration-300;
    @apply hover:bg-white/10;
    @apply border border-white/5;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1),
                0 2px 4px -1px rgba(0, 0, 0, 0.06);
  }

  :global(.event-marker) {
    @apply transition-all duration-200;
    @apply cursor-pointer;
    @apply shadow-lg;
    filter: drop-shadow(0 0 8px rgba(var(--primary), 0.5));
  }

  :global(.event-preview) {
    @apply fixed z-50;
    @apply bg-white/10 backdrop-blur-md;
    @apply rounded-lg p-3;
    @apply border border-white/10;
    @apply shadow-lg;
    @apply text-white;
    @apply pointer-events-none;
    @apply transform -translate-x-1/2;
    @apply transition-all duration-200;
    @apply mt-2;
  }

  .preview-content {
    @apply space-y-1;
  }

  .preview-content h3 {
    @apply text-sm font-medium;
  }

  .preview-content p {
    @apply text-xs text-white/60;
  }
</style>
