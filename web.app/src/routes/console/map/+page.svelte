<script lang="ts">
  import type { PageData } from "./$types";
  import { Button } from "$lib/components/ui/button";
  import type { ShellContext } from "../../../lib/types/types";
  import { _ } from "svelte-i18n";
  import { Search, MapPin, PlusCircle } from "lucide-svelte";
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

  let { data }: { data: PageData } = $props();

  // 选中的事件数据
  let selectedEvent = $state<Event | null>(null);

  // 分类标签
  let categoryItems = $state([
    { id: "all", name: "全部" ,color: "#94a3b8" }
  ]);

  // 事件列表数据
  let events = $state<Event[]>([]);
  let filteredEvents = $state<Event[]>([]);

  let selectedCategory = $state("all");
  let searchQuery = "";
  let currentPage = 1;
  const itemsPerPage = 6;
  let totalPages = 1;

  // 地图相关状态
  let mapInstance: any = null;

  // 页面加载时获取数据
  onMount(() => {
    fetchEvents();
    fetchCategories();
  });

  // 获取分类数据
  async function fetchCategories() {
    try {
      const categories = await categoryStore.fetchCategories();
      console.log('Fetched categories:', categories);
      // 更新分类标签
      categoryItems = [
        ...categories.map(cat => ({
          id: cat.$id,
          name: cat.name.zh,
          color: cat.color
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
      filterEvents();
    } catch (error) {
      console.error('Failed to fetch events:', error);
    }
  }

  // 过滤事件
  function filterEvents() {
    console.log('Filtering events with category:', selectedCategory);
    let filtered = [...events];

    // 按分类过滤
    if (selectedCategory !== "all") {
      filtered = filtered.filter(event => {
        console.log('Checking event:', event.title, 'category:', event.category, 'selected:', selectedCategory);
        return event.category === selectedCategory;
      });
    }

    console.log('Filtered events:', filtered.length);
    filteredEvents = filtered;
    totalPages = Math.ceil(filteredEvents.length / itemsPerPage);
  }

  // 监听分类变化
  // $effect(() => {
  //   filterEvents();
  // });

  function handleCategoryClick(categoryId: string) {
    console.log('Category clicked:', categoryId);
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
    const verticalSpacing = 60;
    return `translate(0, ${index * verticalSpacing}px)`;
  }

  function handleCreateEvent() {
    eventTitle = "";
    eventDescription = "";
    eventLocation = "";
    eventDate = "";
  }

  function handleClosePanel() {
    showCreatePanel = false;
  }

  function handleMapLoad(map: any) {
    console.log('Map loaded:', map);
    mapInstance = map;
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
</script>

<div class="w-full h-screen flex flex-col relative">
  <!-- 地图容器 -->
  <div class="absolute inset-0 z-0">
    <Map 
      on:mapLoad={({ detail }) => handleMapLoad(detail)}
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
  <div class="relative flex-none">
    <!-- 内容区域 -->
    <div class="container mx-auto p-16 space-y-10">
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 class="text-3xl font-bold mb-2">{$_("site.events")}</h1>
          <h2 class="text-sm text-muted-foreground">{$_("events.subtitle")}</h2>
        </div>
        <div class="flex items-center gap-4">
          <Button variant="ghost" size="icon">
            <Search class="h-5 w-5" />
          </Button>
          <Button 
            variant="ghost" 
            size="icon" 
            onclick={() => handleLocationClick()}
          >
            <MapPin class="h-5 w-5" />
          </Button>
        </div>
      </div>

      <!-- 分类标签 -->
      <!-- <TagNav 
        bind:selectedId={selectedCategory}
        items={categoryItems} 
        on:select={({ detail }) => {
          console.log('TagNav select event:', detail);
          filterEvents();
        }}
      /> -->
    </div>
  </div>

  <!-- 底部事件展示区域 -->
  <div class="relative mt-auto mx-auto max-w-[1200px] px-14 mb-6">
    <EventList class="" events={filteredEvents} cardclick={handleEventClick} />
  </div>
</div>
