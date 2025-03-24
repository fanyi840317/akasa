<script lang="ts">
    import {
        Avatar,
        AvatarImage,
        AvatarFallback,
    } from "$lib/components/ui/avatar";
    
    interface EventProps {
        id: string;
        title: string;
        image: string;
        location: string;
        date: string;
    }

    let { event, formatDate, onClick }: {
        event: EventProps;
        formatDate: (date: string) => string;
        onClick?: (params: { event: MouseEvent }) => void;
    } = $props();
    
    function handleClick(event: MouseEvent) {
        onClick?.({ event });
    }
</script>

<div class="relative w-full px-2 py-4">
    <div class="flex items-center p-4 gap-6 group cursor-pointer bg-card/40 shadow-md hover:-translate-y-2 transition-transform hover:shadow-lg rounded-lg w-full" onclick={handleClick}>
        <div class="relative h-16 flex-shrink-0">
            <img src={event.image} alt={event.title} class="h-16 w-16 rounded-full object-cover" />
            <div class="absolute -bottom-2 -right-2">
                <Avatar class="h-8 w-8 border-2 border-background">
                    <AvatarImage src="/images/avatar.png" />
                    <AvatarFallback>U{event.id}</AvatarFallback>
                </Avatar>
            </div>
        </div>
        <div class="flex-1 flex flex-col space-y-1 min-w-0">
            <h3 class="text-sm font-semibold truncate">{event.title}</h3>
            <div class="text-xs text-foreground/60 truncate">
                <span>{event.location}</span>
            </div>
            <div class="text-xs text-foreground/60 truncate">
                <span>{formatDate(event.date)}</span>
            </div>
        </div>
    </div>
</div>
