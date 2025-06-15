
<script>
    import { goto } from '$app/navigation';
    import { Button } from '$lib/components/ui/button';
</script>
<div class="flex-center szie-full">
    <div class="text-center">
        <p class="text-lg font-semibold mb-2">事件未找到</p>
        <p class="text-muted-foreground mb-4">请检查事件ID是否正确</p>
        <Button onclick={() => goto('/console/events')}>返回事件列表</Button>
    </div>
</div>