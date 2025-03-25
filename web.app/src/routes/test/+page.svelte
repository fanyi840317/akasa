<script lang="ts">
    import AffineEditor from "$lib/components/ui/editor/affine-editor.svelte";
    import type { AppState } from "$lib/components/ui/editor/affine-editor";
    import { writable } from "svelte/store";
    import { setContext } from "svelte";
    import EventDetail from "../../lib/components/console/create-event.svelte";

    // 事件属性
    let eventTitle = "测试事件";
    let eventLocation = "测试地点";
    let eventDate = "2024-01-01";
    let eventStatus = "未开始";
    let creator = {
        name: "范一",
        avatar: "https://github.com/shadcn.png"
    };
</script>

<div class="flex p-6 w-full h-[90vh] bg-card">
    <EventDetail
        {eventTitle}
        {eventLocation}
        {eventDate}
        {eventStatus}
        {creator}
    />
</div>