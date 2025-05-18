<script lang="ts">
    import { UserAvatar } from "$lib/components/ui/avatar";

    interface Props {
        title: string;
        description: string;
        duration: string;
        src?: string;
        fallback?: string;
        onClick?: () => void;
        onDblClick?: () => void;
        isSelected?: boolean;
    }

    let { title, description, duration, src, fallback, onClick, onDblClick, isSelected }: Props =
        $props();
</script>

<!-- svelte-ignore a11y_click_events_have_key_events -->
<!-- svelte-ignore a11y_no_static_element_interactions -->
<div
    class="card bg-base-100 card-border border-base-300 card-sm overflow-hidden coursor-pointer
    hover:shadow-xl hover:shadow-primary/50 hover:scale-105 transition-all duration-300
    min-w-[300px] max-w-[400px] min-h-[200px]"
    class:ring-1={isSelected}
    onclick={onClick}
    ondblclick={onDblClick}
>
    <div class="card-body gap-4">
        <figure></figure>
    </div>
    <div class="bg-base-300">
        <div class="flex items-center gap-2 p-4">
            <div class="grow">
                <div class="text-sm font-medium truncate whitespace-nowrap">
                    {title}
                </div>
                <div class="text-xs opacity-60 line-clamp-2">
                    {description}
                </div>
            </div>
            <div class="shrink-0">
                <UserAvatar class="size-6" {src} {fallback}></UserAvatar>
            </div>
        </div>
    </div>
</div>
