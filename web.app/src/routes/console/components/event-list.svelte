<script lang="ts">
    import { cn } from "$lib/utils";
    import * as Carousel from "$lib/components/ui/carousel";
    import EventCard from "./event-card.svelte";
    import { createEventDispatcher } from "svelte";
    
    const dispatch = createEventDispatcher();

    let {
        events = [],
        class: className = "",
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

    function onClick(event: CustomEvent) {
        const { detail } = event;
        // 触发父组件处理卡片点击事件
        dispatch("cardclick", detail);
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
            {#each events as event, i (event.id)}
                <Carousel.Item class="md:basis-1/2 lg:basis-1/4 pl-0">
                    <EventCard {event} {formatDate} onClick={onClick} />
                </Carousel.Item>
            {/each}
        </Carousel.Content>
    </div>
    <Carousel.Previous class="z-20" />
    <Carousel.Next class="z-20" />
</Carousel.Root>
