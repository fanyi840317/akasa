<script lang="ts">
    import { fade } from "svelte/transition";
    import { flip } from "svelte/animate";
    import { cn } from "$lib/utils";
    import * as HoverCard from "$lib/components/ui/hover-card";
    import * as Card from "$lib/components/ui/card";
    import * as Carousel from "$lib/components/ui/carousel";
    import EventCard from "./event-card.svelte";

    let {
        events = [],
        class: className = '',
    }: {
        events: Array<{
            id: string;
            title: string;
            image: string;
            tags: string[];
            location: string;
            date: string;
            attendees: number;
            rating: number;
        }>;
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

    // 为卡片内容元素添加交错动画的延迟函数
    function getStaggerDelay(i: number) {
        return i * 50; // 每个元素延迟50ms
    }
</script>

<Carousel.Root
opts={{
    align: "start",
}}
class={cn("p-4 relative", className)}
>
<div class="absolute -left-20 top-0 bottom-0 w-[30%] bg-gradient-to-r from-background via-background/50 to-transparent z-10 pointer-events-none" />
<div class="absolute -right-20 top-0 bottom-0 w-[30%] bg-gradient-to-l from-background via-background/50 to-transparent z-10 pointer-events-none" />
<Carousel.Content class="-ml-4">
    {#each events as event, i (event.id)}
        <Carousel.Item class="md:basis-1/2 lg:basis-1/4 pl-4">
                    <EventCard {event} {formatDate} />
        </Carousel.Item>
    {/each}
</Carousel.Content>
<Carousel.Previous class="z-20" />
<Carousel.Next class="z-20" />
</Carousel.Root>
