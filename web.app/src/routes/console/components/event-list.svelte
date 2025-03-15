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
<Carousel.Content class="-ml-4">
    {#each events as event, i (event.id)}
        <Carousel.Item class="md:basis-1/2 lg:basis-1/4 pl-4">
            <HoverCard.Root>
                <HoverCard.Trigger>
                    <EventCard {event} {formatDate} />
                </HoverCard.Trigger>
                <HoverCard.Content
                    sideOffset={-100}
                    class="w-[400px] p-0"
                >
                    <EventCardHover
                        {event}
                        {formatDate}
                        {getStaggerDelay}
                    />
                </HoverCard.Content>
            </HoverCard.Root>
        </Carousel.Item>
    {/each}
</Carousel.Content>
<Carousel.Previous class="backdrop-blur-sm bg-gradient-to-r from-transparent via-background/30 to-transparent" />
<Carousel.Next class="backdrop-blur-sm bg-gradient-to-r from-transparent via-background/30 to-transparent" />
</Carousel.Root>
