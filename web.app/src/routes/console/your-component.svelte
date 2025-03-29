<script lang="ts">
    import { getContext } from 'svelte';

    interface EventPanelContext {
        openEvent: (event: {
            title: string;
            time: string;
            status: string;
            content: string;
        }) => void;
    }

    // 获取事件面板上下文
    const { openEvent } = getContext<EventPanelContext>('eventPanel');

    // 示例事件数据
    const event = {
        title: "通知标题",
        time: "2024-03-20 10:00",
        status: "未读",
        content: "这是通知的详细内容..."
    };

    // 处理卡片点击
    function handleCardClick() {
        openEvent(event);
    }
</script>

<div class="cursor-pointer" on:click={handleCardClick}>
    <div class="p-4 rounded-sm border bg-card hover:bg-muted/50 transition-colors">
        <h3 class="font-medium">{event.title}</h3>
        <p class="text-sm text-muted-foreground">{event.time}</p>
    </div>
</div> 