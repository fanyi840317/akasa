<script lang="ts">
  import { Badge } from "$lib/components/ui/badge";
  import { Button } from "$lib/components/ui/button";
  import { Avatar, AvatarFallback, AvatarImage } from "$lib/components/ui/avatar";
  import type { Evidence } from '$lib/types/event';
  import { PlusCircle, CheckCircle2, XCircle } from 'lucide-svelte';
  import { _ } from 'svelte-i18n';

  export let evidence: Evidence[];
</script>

<div class="space-y-6">
  <div class="flex items-center justify-between">
    <div class="flex items-center gap-2">
      <h2 class="text-2xl font-semibold">{$_('events.evidence')}</h2>
      <span class="text-sm text-muted-foreground">({evidence.length})</span>
    </div>
    <Button variant="outline" size="sm" class="gap-2">
      <PlusCircle class="w-4 h-4" />
      {$_('events.submit_evidence')}
    </Button>
  </div>

  <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
    {#each evidence as item}
      <div class="flex flex-col rounded-lg overflow-hidden bg-secondary hover:shadow-lg transition-all duration-300 relative">
        <!-- 媒体内容 -->
        <div class="aspect-video">
          {#if item.type === 'image'}
            <img src={item.url} alt={item.description} class="w-full h-full object-cover" />
          {:else if item.type === 'video'}
            <video src={item.url} class="w-full h-full object-cover" controls />
          {/if}
        </div>

        <!-- 验证状态标签 -->
        <Badge variant={item.verified ? 'default' : 'destructive'} class="absolute top-2 right-2 bg-background/80 inline-flex items-center gap-1">
          {#if item.verified}
            <CheckCircle2 class="w-3 h-3" />
            已验证
          {:else}
            <XCircle class="w-3 h-3" />
            未验证
          {/if}
        </Badge>

        <!-- 描述和提交者信息 -->
        <div class="p-3 space-y-2">
          <!-- <p class="text-sm line-clamp-2"></p> -->
          <div class="flex items-center gap-2">
            <Avatar class="w-6 h-6">
              {#if item.submitter?.avatar}
                <AvatarImage src={item.submitter.avatar} alt={item.submitter.name} />
              {/if}
              <AvatarFallback>{item.submitter?.name?.[0] ?? '?'}</AvatarFallback>
            </Avatar>
            <span class="text-xs">{item.description ?? '未知提交者'}</span>
          </div>
        </div>
      </div>
    {/each}
  </div>
</div>