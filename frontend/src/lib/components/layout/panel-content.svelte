<script lang="ts">
    export let title: string = '';
    export let time: string = '';
    export let status: string = '';
    export let content: string = '';
</script>

<div class="space-y-4">
    <div class="prose dark:prose-invert">
        <h3 class="text-lg font-medium">{title}</h3>
        <div class="flex gap-4 text-sm text-muted-foreground">
            <span>{time}</span>
            <span>{status}</span>
        </div>
        <div class="mt-4">
            {content}
        </div>
    </div>
</div>
