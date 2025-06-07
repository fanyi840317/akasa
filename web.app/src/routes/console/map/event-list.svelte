<script lang="ts">
  import { cn } from "$lib/utils";
  import * as Carousel from "$lib/components/ui/carousel";
  import type { Event } from "$lib/types/event";
  import {
    Avatar,
    AvatarImage,
    AvatarFallback,
  } from "$lib/components/ui/avatar";
  import { Calendar, MapPin, User } from "lucide-svelte";

  let {
    events = [],
    class: className = "",
    cardclick,
  }: {
    events: Event[];
    class?: string;
    cardclick?: (event: Event) => void;
  } = $props();

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
      creator_avatar: "/images/avatars/avatar1.png"
    },
    {
      $id: "2",
      $createdAt: new Date().toISOString(),
      $updatedAt: new Date().toISOString(),
      title: "消失的街道",
      content: "一条街道在深夜突然消失，第二天早上又出现...",
      location: "上海市浦东新区",
      date: new Date().toISOString(),
      user_id: "user2",
      is_public: true,
      cover_image: "/images/cover/c2.webp",
      status: "unverified",
      category: "paranormal",
      creator_name: "都市传说",
      creator_avatar: "/images/avatars/avatar2.png"
    },
    {
      $id: "3",
      $createdAt: new Date().toISOString(),
      $updatedAt: new Date().toISOString(),
      title: "时间异常区域",
      content: "某区域的时间流速异常，手表显示时间比实际时间快/慢...",
      location: "广州市天河区",
      date: new Date().toISOString(),
      user_id: "user3",
      is_public: true,
      cover_image: "/images/cover/c3.webp",
      status: "unverified",
      category: "supernatural",
      creator_name: "时间观察者",
      creator_avatar: "/images/avatars/avatar3.png"
    }
  ];

  // 如果没有提供事件数据，使用模拟数据
  if (events.length === 0) {
    events = mockEvents;
  }

  // 获取随机默认封面图
  function getRandomDefaultCover(): string {
    const defaultCovers = [
      '/images/cover/c1.webp',
      '/images/cover/c2.webp',
      '/images/cover/c3.webp'
    ];
    const randomIndex = Math.floor(Math.random() * defaultCovers.length);
    return defaultCovers[randomIndex];
  }

  function formatDate(dateString: string | undefined) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString("zh-CN", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  }

  function handleEventClick(event: Event) {
    if (cardclick) {
      cardclick(event);
    }
  }

  function handleImageError(event: Event) {
    event.cover_image = getRandomDefaultCover();
  }
</script>

<Carousel.Root
  opts={{
    align: "start",
  }}
  class={cn("p-4 relative", className)}
>
  <div class="relative overflow-hidden">
    <Carousel.Content
      class="-ml-4"
      style="mask-image: linear-gradient(to right, transparent 0%, hsl(var(--foreground)) 3%, hsl(var(--foreground)) 97%, transparent 100%); -webkit-mask-image: linear-gradient(to right, transparent 0%, hsl(var(--foreground)) 3%, hsl(var(--foreground)) 97%, transparent 100%);"
    >
      {#each events as event}
        <Carousel.Item class="md:basis-1/2 lg:basis-1/4 pl-0">
          <div class="relative w-full px-2 py-4">
            <div
              class="event-card"
              on:click={() => handleEventClick(event)}
            >
              <div class="event-image-wrapper">
                <img
                  src={event.cover_image || getRandomDefaultCover()}
                  alt={event.title}
                  class="event-image"
                  on:error={() => handleImageError(event)}
                />
                <div class="event-creator">
                  <Avatar class="h-8 w-8 shadow-lg">
                    <AvatarImage 
                      src={event.creator_avatar} 
                      alt={event.creator_name}
                      class="object-cover"
                    />
                    <AvatarFallback class="bg-primary/10 text-primary">
                      <User class="h-4 w-4" />
                    </AvatarFallback>
                  </Avatar>
                </div>
              </div>
              <div class="event-content">
                <h3 class="event-title">
                  {event.title}
                </h3>
                <div class="event-details">
                  <div class="event-detail-item">
                    <MapPin class="h-3 w-3" />
                    <span>{event.location}</span>
                  </div>
                  <div class="event-detail-item">
                    <Calendar class="h-3 w-3" />
                    <span>{formatDate(event.date)}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </Carousel.Item>
      {/each}
    </Carousel.Content>
  </div>
  <div class="carousel-controls">
    <Carousel.Previous class="carousel-button" />
    <Carousel.Next class="carousel-button" />
  </div>
</Carousel.Root>

<style lang="postcss">
  .event-card {
    @apply flex items-center p-4 gap-6 cursor-pointer;
    @apply bg-white/5 backdrop-blur-md rounded-xl;
    @apply transition-all duration-300;
    @apply hover:bg-white/10;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1),
                0 2px 4px -1px rgba(0, 0, 0, 0.06),
                inset 0 0 0 1px rgba(255, 255, 255, 0.1);
  }

  .event-image-wrapper {
    @apply relative h-16 flex-shrink-0;
  }

  .event-image {
    @apply h-16 w-16 rounded-xl object-cover;
    @apply transition-all duration-300;
    box-shadow: 0 4px 8px -2px rgba(0, 0, 0, 0.2);
  }

  .event-card:hover .event-image {
    @apply rounded-lg;
    transform: scale(1.05);
  }

  .event-creator {
    @apply absolute -bottom-2 -right-2;
    @apply transition-all duration-300;
    @apply hover:scale-110;
  }

  .event-card:hover .event-creator {
    @apply -translate-y-1;
    box-shadow: 0 4px 12px -2px rgba(0, 0, 0, 0.2);
  }

  .event-content {
    @apply flex-1 flex flex-col space-y-1 min-w-0;
  }

  .event-title {
    @apply text-sm font-semibold text-white/90;
    @apply truncate;
  }

  .event-details {
    @apply flex flex-col gap-1;
  }

  .event-detail-item {
    @apply flex items-center gap-2 text-xs text-white/60;
    @apply truncate;
  }

  .carousel-controls {
    @apply absolute top-1/2 -translate-y-1/2 w-full;
    @apply flex justify-between px-4 pointer-events-none;
  }

  .carousel-button {
    @apply pointer-events-auto;
    @apply bg-white/5 backdrop-blur-md rounded-full p-2;
    @apply hover:bg-white/10 transition-colors;
    @apply text-white/80 hover:text-white;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1),
                0 2px 4px -1px rgba(0, 0, 0, 0.06);
  }

  :global(.dark) {
    color-scheme: dark;
  }
</style>
