<script lang="ts">
  import type { PageData } from "./$types";
  import { Button } from "$lib/components/ui/button";
  import type { ShellContext } from "../../../lib/types/types";
  import { _ } from "svelte-i18n";
  import { Search, MapPin, PlusCircle } from "lucide-svelte";
  import {MapBase as Map} from "$lib/components/ui/map";
  import EventList from "./event-list.svelte";
  import CategoryList from "./category-list.svelte";
  import { getContext, setContext } from "svelte";
  import { writable } from "svelte/store";
  import { goto } from "$app/navigation";
  import { categoryStore } from "$lib/stores/category";
  import { eventStore } from "$lib/stores/event";
  import type { Category } from "$lib/types/category";
  import type { Event } from "$lib/types/event";

  let { data }: { data: PageData } = $props();

  // 选中的事件数据
  let selectedEvent = $state<Event | null>(null);

  // 地点分类数据
  let placeCategories = $state([
    { id: "all", name: "全部", count: 0 }
  ]);

  // 事件列表数据
  let events = $state<Event[]>([]);

  let selectedCategory = "all";
  let searchQuery = "";
  let currentPage = 1;
  const itemsPerPage = 6;
  let totalPages = 1;

  // 创建事件相关状态
  let showCreatePanel = $state(false);
  let eventTitle = $state("");
  let eventDescription = $state("");
  let eventLocation = $state("");
  let eventDate = $state("");
  let eventStatus = $state("未开始");

  // 事件属性
  let eventProperties = [
    { label: "状态", value: "未开始", icon: true, color: "bg-gray-400" },
    { label: "负责人", value: "空白", icon: true, color: "bg-gray-200" },
    { label: "优先级", value: "空白", icon: true, color: "bg-gray-400" },
    { label: "截止日期", value: eventDate || "未设置", icon: false },
  ];

  // 获取分类数据
  async function fetchCategories() {
    try {
      const categories = await categoryStore.fetchCategories();
      // 更新地点分类数据
      placeCategories = [
        { id: "all", name: "全部", count: events.length },
        ...categories.map(cat => ({
          id: cat.$id,
          name: cat.name.zh,
          count: events.filter(event => event.category === cat.$id).length
        }))
      ];
    } catch (error) {
      console.error('Failed to fetch categories:', error);
    }
  }

  // 获取事件数据
  async function fetchEvents() {
    try {
      const fetchedEvents = await eventStore.fetchEvents();
      events = fetchedEvents;
      totalPages = Math.ceil(events.length / itemsPerPage);
    } catch (error) {
      console.error('Failed to fetch events:', error);
    }
  }

  // 页面加载时获取数据
  $effect(() => {
    fetchEvents();
    fetchCategories();
  });

  function handleCategoryClick(categoryId: string) {
    selectedCategory = categoryId;
    currentPage = 1;
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
    const verticalSpacing = 60; // 每个项目之间的垂直间距
    return `translate(0, ${index * verticalSpacing}px)`;
  }

  function handleCreateEvent() {
    // 处理创建事件的逻辑
    eventTitle = "";
    eventDescription = "";
    eventLocation = "";
    eventDate = "";
  }

  function handleClosePanel() {
    showCreatePanel = false;
  }
</script>

<div class="w-full h-screen overflow-hidden">
  <!-- 左侧分类列表 -->
  <div class="absolute left-16 top-[180px] z-20">
    <CategoryList
      categories={placeCategories}
      {selectedCategory}
      onClick={handleCategoryClick}
    />
  </div>

  <div class="absolute top-14 left-14 z-20 p-4">
    <h1 class="text-3xl font-bold mb-2">{$_("site.events")}</h1>
    <h2 class="text-sm text-muted-foreground">{$_("events.subtitle")}</h2>
  </div>

  <!-- 右上角搜索框 -->
  <div class="absolute top-16 right-14 z-20 flex items-center gap-4">
    <Button variant="ghost" size="icon">
      <Search class="h-5 w-5" />
    </Button>
    <Button variant="ghost" size="icon">
      <MapPin class="h-5 w-5" />
    </Button>
  </div>

  <!-- 地图容器 -->
  <div class="absolute inset-0 z-0">
    <Map />
  </div>
  <!-- 黑雾蒙层 -->
  <div
    class="absolute inset-0 z-10 pointer-events-none"
    style="background: radial-gradient(circle at center, transparent 30%, rgba(0, 0, 0, 0.2) 50%, rgba(0, 0, 0, 0.9) 100%)"
  ></div>

  <!-- 底部事件展示区域 -->
  <div
    class="absolute bottom-6 left-0 right-0 z-20 mx-auto max-w-[1200px] px-14"
  >
    <EventList class="" {events} cardclick={handleEventClick} />
  </div>
</div>
