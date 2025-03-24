<script lang="ts">
  import { cn } from "$lib/utils";
  import * as Carousel from "$lib/components/ui/carousel";
  import EventCard from "./event-card.svelte";
  import { createEventDispatcher } from "svelte";

  import {
    Avatar,
    AvatarImage,
    AvatarFallback,
  } from "$lib/components/ui/avatar";
  import type { Event } from "$lib/types/event";

  let {
    events = [],
    class: className = "",
  }: {
    events: Event[];
    class?: string;
  } = $props();

  function formatDate(dateString: string) {
    const date = new Date(dateString);
    return date.toLocaleDateString("zh-CN", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  }

  function onClick(event: CustomEvent) {
    const { detail } = event;

    // 触发父组件处理卡片点击事件
    // dispatch("cardclick", detail);
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
              class="flex items-center p-4 gap-6 group cursor-pointer bg-card/40 shadow-md hover:-translate-y-2 transition-transform hover:shadow-lg rounded-lg w-full"
              onclick={handleClick}
            >
              <div class="relative h-16 flex-shrink-0">
                <img
                  src={event.cover}
                  alt={event.title}
                  class="h-16 w-16 rounded-full object-cover"
                />
                <div class="absolute -bottom-2 -right-2">
                  <Avatar class="h-8 w-8 border-2 border-background">
                    <AvatarImage src={event.creator_avatar} />
                    <AvatarFallback>{event.creator_name}</AvatarFallback>
                  </Avatar>
                </div>
              </div>
              <div class="flex-1 flex flex-col space-y-1 min-w-0">
                <h3 class="text-sm font-semibold truncate">
                  {event.title}
                </h3>
                <div class="text-xs text-foreground/60 truncate">
                  <span>{event.location}</span>
                </div>
                <div class="text-xs text-foreground/60 truncate">
                  <span>{formatDate(event.date)}</span>
                </div>
              </div>
            </div>
          </div>
        </Carousel.Item>
      {/each}
    </Carousel.Content>
  </div>
  <Carousel.Previous class="z-20" />
  <Carousel.Next class="z-20" />
</Carousel.Root>
