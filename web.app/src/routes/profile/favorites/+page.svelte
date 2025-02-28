<script lang="ts">
  import { _ } from 'svelte-i18n';
  import { Button } from "$lib/components/ui/button";
  import { Card } from "$lib/components/ui/card";
  import { Badge } from "$lib/components/ui/badge";
  import { Bookmark } from "lucide-svelte";

  // 模拟收藏事件数据
  let favoriteEvents = [
    {
      id: 1,
      title: '城市街道安全隐患',
      description: '发现某十字路口信号灯故障',
      status: 'open',
      category: '交通安全',
      createdAt: new Date('2024-01-15'),
      location: '广州市天河区'
    },
    {
      id: 2,
      title: '社区环境问题',
      description: '小区垃圾分类设施损坏',
      status: 'resolved',
      category: '环境保护',
      createdAt: new Date('2024-01-10'),
      location: '广州市海珠区'
    }
  ];

  function removeFavorite(eventId: number) {
    // TODO: 实现取消收藏逻辑
    console.log('取消收藏事件:', eventId);
    favoriteEvents = favoriteEvents.filter(event => event.id !== eventId);
  }

  function getStatusColor(status: string) {
    return status === 'resolved' ? 'bg-green-500' : 'bg-blue-500';
  }
</script>

<div class="space-y-6">
  <div class="flex items-center justify-between">
    <div>
      <h3 class="text-lg font-medium">{$_('profile.favorites')}</h3>
      <p class="text-sm text-muted-foreground">{$_('profile.favorites_desc')}</p>
    </div>
  </div>

  <div class="grid gap-4">
    {#each favoriteEvents as event (event.id)}
      <Card class="p-4">
        <div class="flex items-start justify-between">
          <div class="space-y-2 flex-1">
            <div class="flex items-center justify-between">
              <h4 class="text-base font-semibold">{event.title}</h4>
              <Button
                variant="ghost"
                size="icon"
                class="text-muted-foreground hover:text-destructive"
                on:click={() => removeFavorite(event.id)}
              >
                <Bookmark class="h-4 w-4" />
              </Button>
            </div>
            <p class="text-sm text-muted-foreground">{event.description}</p>
            <div class="flex items-center gap-2 text-xs text-muted-foreground">
              <Badge variant="secondary">{event.category}</Badge>
              <span>{event.location}</span>
              <span>•</span>
              <span>{event.createdAt.toLocaleDateString()}</span>
            </div>
          </div>
        </div>
      </Card>
    {/each}

    {#if favoriteEvents.length === 0}
      <div class="text-center py-8 text-muted-foreground">
        {$_('profile.no_favorites')}
      </div>
    {/if}
  </div>
</div>