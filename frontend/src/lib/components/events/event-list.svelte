<script lang="ts">
    import EventItem from "./event-item.svelte";
    import type { Event } from "$lib/types/event";

    // let events: Array<{
    //     title: string;
    //     description: string;
    //     createdBy: string;
    //     credibilityScore: number;
    //     occurredAt: string;
    //     evidence?: Array<{
    //         url: string;
    //         description: string;
    //     }>;
    // }>;
    // export let users: Record<string, { name: string }>;
    let { events, onclick } = $props<{
        events: Event | null;
        onclick: (event: Event) => void;
    }>();
</script>

<div class="flex gap-1.5 flex-col ">
    <!-- Header -->
    <div
        class="flex items-stretch justify-start  overflow-hidden pl-4 rounded-2xl"
    >
        <div
            class="event-cell flex-center text-base-content/20 font-semibold text-xs w-4/12"
        >
            事件信息
        </div>
        <div
            class="event-cell w-1/12 min-w-28 border-base-content/20 flex-center text-base-content/20 font-semibold text-xs"
        >
            所有者
        </div>
        <div
            class="event-cell w-1/12 min-w-28 flex-center border-base-content/20 text-base-content/20 font-semibold text-xs"
        >
            可信度
        </div>
        <div
            class="event-cell w-1/12 min-w-28 flex-center border-base-content/20 text-base-content/20 font-semibold text-xs"
        >
            发生时间
        </div>
        <div
            class="w-fill ml-2 flex-1 min-w-28 border-l-4 border-base-content/20 flex-center text-base-content/20 uppercase font-semibold text-xs"
        >
            证据
        </div>
    </div>

    <!-- Events List -->
    {#each events as event, index}
        <EventItem {event} isEven={index % 2 === 0} {onclick} />
    {/each}
</div>

<style>
    @layer base {
        .event-cell {
            @apply w-1/12 border-l-4 border-transparent uppercase   hidden;
        }
    }
</style>
