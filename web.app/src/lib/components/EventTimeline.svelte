<script lang="ts">
  import { Badge } from "$lib/components/ui/badge";
  import { Button } from "$lib/components/ui/button";
  import { Avatar, AvatarFallback, AvatarImage } from "$lib/components/ui/avatar";
  import type { Event } from '$lib/types/event';
  import { PlusCircle } from 'lucide-svelte';
  import { _ } from 'svelte-i18n';

  export let event: Event;
</script>

<div class="space-y-6">
  <div class="flex items-center justify-between">
    <h2 class="text-2xl font-semibold">{$_('events.timeline')}</h2>
    <Button variant="outline" size="sm" class="gap-2">
      <PlusCircle class="w-4 h-4" />
      {$_('events.submit_evidence')}
    </Button>
  </div>

<div class="relative pl-8 space-y-8">
  <div class="absolute left-[10px] top-0 bottom-0 w-0.5 bg-border"></div>
  {#each event.timeline as item}
    <div class="relative">
      <div class="absolute -left-[28px] w-4 h-4 rounded-full bg-primary ring-4 ring-primary/20" />
      <div class="space-y-4">
        <div class="flex items-center gap-2">
          <div class="text-sm font-medium text-primary">{item.timestamp.toLocaleString()}</div>
        </div>
        
        <p class="text-lg font-medium">{item.description}</p>

        <!-- 证据展示 -->
        {#if item.evidenceIds.length > 0}
          <div class="mt-4 grid grid-cols-2 md:grid-cols-3 gap-4">
            {#each item.evidenceIds as evidenceId}
              {#if event.evidence.find(e => e.id === evidenceId)}
                {@const evidence = event.evidence.find(e => e.id === evidenceId)}
                <div class="flex flex-col rounded-lg overflow-hidden bg-secondary hover:shadow-lg transition-all duration-300 relative">
                  <div class="absolute top-2 left-2 z-10 flex items-center gap-2">
                    <Avatar class="w-8 h-8 border-2 border-background">
                      <AvatarImage src={`https://api.dicebear.com/7.x/avataaars/svg?seed=${evidence?.submittedBy}`} />
                      <AvatarFallback>{evidence?.submittedBy[0]?.toUpperCase()}</AvatarFallback>
                    </Avatar>
                    <span class="text-xs font-medium text-background/90 drop-shadow-md">{evidence?.submittedBy}</span>
                  </div>
                  <div class="aspect-video">
                    {#if evidence?.type === 'image'}
                      <img src={evidence.url} alt={evidence.description} class="w-full h-full object-cover" />
                    {:else if evidence?.type === 'video'}
                      <video src={evidence.url} controls class="w-full h-full object-cover" />
                    {/if}
                  </div>
                  <Badge variant="secondary" class="bg-background/80 absolute top-2 right-2">
                    {evidence?.verificationStatus ? '已验证' : '待验证'}
                  </Badge>
                  <div class="p-3">
                    <p class="text-sm text-muted-foreground line-clamp-2">{evidence?.description}</p>
                  </div>
                </div>
              {/if}
            {/each}
          </div>
        {/if}
      </div>
    </div>
  {/each}
</div>
</div>
