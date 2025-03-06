<script lang="ts">
  import { Avatar, AvatarFallback, AvatarImage } from "$lib/components/ui/avatar";
  import { Badge } from "$lib/components/ui/badge";
  import { Button } from "$lib/components/ui/button";
  import * as Card from "$lib/components/ui/card";
  import type { Witness } from '$lib/types/event';
  import { PlusCircle } from 'lucide-svelte';
  import { _ } from 'svelte-i18n';

  export let witnesses: Witness[];
</script>

<div class="space-y-6">
  <div class="flex items-center justify-between">
    <div class="flex items-center gap-2">
      <h2 class="text-2xl font-semibold">{$_('events.witnesses')}</h2>
      <span class="text-sm text-muted-foreground">({witnesses.length})</span>
    </div>
    <Button variant="outline" size="sm" class="gap-2">
      <PlusCircle class="w-4 h-4" />
      {$_('events.submit_witness')}
    </Button>
  </div>

  <div class="space-y-6">
    {#each witnesses as witness}
      <div class="flex items-start gap-3">
        <Avatar class="w-10 h-10 mt-1">
          {#if witness.avatar && !witness.anonymous}
            <AvatarImage src={witness.avatar} alt={witness.name} />
          {/if}
          <AvatarFallback>{witness.anonymous ? '?' : witness.name[0]}</AvatarFallback>
        </Avatar>
        
        <div class="flex-1 space-y-2">
          <div class="flex items-center gap-2">
            <!-- <span class="font-medium">{witness.anonymous ? '匿名目击者' : witness.name}</span> -->
            {#if witness.credibilityScore}
              <Badge variant="outline" class="bg-primary/10">
                可信度 {witness.credibilityScore}%
              </Badge>
            {/if}
          </div>
          
          <div class="relative">
            <div class="absolute -left-2 top-4 w-3 h-3 rotate-45 bg-secondary/10"></div>
            <div class="p-4 rounded-lg bg-secondary/10 shadow-sm">
              <p class="text-sm leading-relaxed">{witness.testimony}</p>
              <div class="mt-2 text-xs text-muted-foreground">
                {new Date(witness.timestamp).toLocaleString()}
                {#if witness.location}
                  · {witness.location}
                {/if}
              </div>
            </div>
          </div>
        </div>
      </div>
    {/each}
  </div>
</div>