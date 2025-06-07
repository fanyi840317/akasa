<script lang="ts">
    import { Avatar, AvatarFallback, AvatarImage } from "$lib/components/ui/avatar";
    
    export let clues: Array<{
        id: string;
        title: string;
        cover?: string;
        creator?: {
            name: string;
            avatar?: string;
        };
    }> = [];
    
    // 限制显示数量
    const MAX_VISIBLE = 3;
    const visibleClues = clues.slice(0, MAX_VISIBLE);
    const remainingCount = Math.max(0, clues.length - MAX_VISIBLE);
</script>

<div class="relative h-[120px] flex items-end">
    {#each visibleClues as clue, i (clue.id)}
        <div 
            class="absolute rounded-lg border bg-card shadow-sm overflow-hidden transition-all duration-300 hover:translate-y-[-8px]"
            style="width: 200px; height: 100px; left: {i * 40}px; z-index: {10 - i};"
        >
            <!-- 卡片内容 -->
            <div class="relative h-full">
                {#if clue.cover}
                    <img src={clue.cover} alt={clue.title} class="w-full h-full object-cover opacity-20" />
                {/if}
                <div class="absolute inset-0 bg-gradient-to-t from-background to-background/20" />
                <div class="absolute bottom-2 left-2 right-2">
                    <p class="text-sm font-medium truncate">{clue.title}</p>
                    {#if clue.creator}
                        <div class="flex items-center gap-2 mt-1">
                            <Avatar class="h-5 w-5">
                                {#if clue.creator.avatar}
                                    <AvatarImage src={clue.creator.avatar} alt={clue.creator.name} />
                                {/if}
                                <AvatarFallback class="text-[10px]">
                                    {clue.creator.name?.[0] || "?"}
                                </AvatarFallback>
                            </Avatar>
                            <span class="text-xs text-muted-foreground">{clue.creator.name}</span>
                        </div>
                    {/if}
                </div>
            </div>
        </div>
    {/each}
    
    {#if remainingCount > 0}
        <div 
            class="absolute flex items-center justify-center rounded-lg border bg-card/50 backdrop-blur-sm"
            style="width: 200px; height: 100px; left: {MAX_VISIBLE * 40}px; z-index: {10 - MAX_VISIBLE};"
        >
            <span class="text-lg font-medium text-muted-foreground">+{remainingCount}</span>
        </div>
    {/if}
</div>