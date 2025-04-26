<script lang="ts">
  import { Sparkles } from "lucide-svelte";
  import BorderBeam from "$lib/components/ui/background/border-beam.svelte";
  
  export let title = "";
  export let image = "";
  export let tags: string[] = [];
</script>

<div class="mx-4 w-[280px] flex-shrink-0">
  <article class="relative rounded-2xl border border-gray-700/70 bg-black/60 backdrop-blur-sm overflow-hidden transition-all duration-300 hover:border-purple-500/50 hover:shadow-[0_0_15px_rgba(99,68,245,0.3)]">
    <BorderBeam size={80} duration={10} />
    <div class="p-4">
      <div class="relative w-full h-24 rounded-lg overflow-hidden mb-3">
        {#if image}
          <img 
            src={image} 
            alt={title}
            class="w-full h-full object-cover transition-transform duration-500 hover:scale-110"
          />
          <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
        {:else}
          <div class="w-full h-full bg-purple-900/20 flex items-center justify-center">
            <Sparkles class="h-6 w-6 text-purple-400/50" />
          </div>
        {/if}
      </div>
      
      <h3 class="text-base font-medium text-gray-200 line-clamp-1 hover:text-purple-300 transition-colors">
        {title}
      </h3>
      
      <div class="flex gap-2 mt-2 flex-wrap">
        {#if tags && tags.length > 0}
          {#each tags.slice(0, 2) as tag}
            <span class="px-2 py-0.5 text-xs rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-300">
              {tag}
            </span>
          {/each}
          {#if tags.length > 2}
            <span class="px-2 py-0.5 text-xs rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-300">
              +{tags.length - 2}
            </span>
          {/if}
        {/if}
      </div>
    </div>
  </article>
</div>
