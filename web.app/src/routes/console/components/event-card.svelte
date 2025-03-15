<script lang="ts">
    import {
        Avatar,
        AvatarImage,
        AvatarFallback,
    } from "$lib/components/ui/avatar";
    
    let { event, formatDate }: {
        event: {
            id: string;
            title: string;
            image: string;
            location: string;
            date: string;
        };
        formatDate: (date: string) => string;
    } = $props();
</script>

<style>
    .event-card {
        @apply relative w-full px-2 transition-all duration-100 hover:z-10 hover:-translate-y-1 cursor-pointer;
    }
    .event-card:hover .event-content {
        @apply scale-[1.2] bg-cover bg-center;
    }
    .event-card:hover .event-title {
        @apply text-primary;
    }
    .event-content {
        @apply relative bg-card/20 flex items-center p-4 gap-6 transition-all duration-300;
    }
    .event-title {
        @apply text-sm text-gray-300 transition-colors duration-300;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
    }
    .event-info {
        @apply text-xs text-gray-300/40;
        text-shadow: 0 1px 1px rgba(0, 0, 0, 0.3);
    }
</style>

<div class="event-card">
    <div class="event-content" style="background-image: ">
        <div class="relative h-16 flex-shrink-0">
            <img src={event.image} alt={event.title} class="w-full h-full rounded-full object-cover" />
            <div class="absolute -bottom-2 -right-2">
                <Avatar class="h-8 w-8 border-2 border-background">
                    <AvatarImage src="/images/avatar.png" />
                    <AvatarFallback>U{event.id}</AvatarFallback>
                </Avatar>
            </div>
        </div>
        <div class="flex-1 flex flex-col space-y-1">
            <h3 class="event-title font-semibold">{event.title}</h3>
            <div class="event-info">
                <span>{event.location}</span>
            </div>
            <div class="event-info">
                    <span>{formatDate(event.date)}</span>
                </div>
            </div>
        </div>
    </div>