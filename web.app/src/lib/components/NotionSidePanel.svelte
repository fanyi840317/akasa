<script lang="ts">
  import { cn } from "$lib/utils";
  import { Button } from "$lib/components/ui/button";
  import { ChevronRight, ChevronLeft, X } from "lucide-svelte";
  import { fade, fly } from 'svelte/transition';

  export let isOpen = false;
  export let title = "";
  export let onClose = () => {};
</script>

{#if isOpen}
<div class="fixed inset-0 z-[100]" transition:fade={{ duration: 150 }}>
  <!-- Backdrop with click to close -->
  <div class="absolute inset-0 bg-black/20 backdrop-blur-sm" onclick={onClose}></div>
  
  <!-- Right side panel -->
  <div 
    class="absolute top-0 right-0 h-full w-full sm:w-[550px] lg:w-[650px] bg-background" 
    transition:fly={{ x: 300, duration: 200, opacity: 1 }}
  >
    <div class="flex h-full flex-col">
      <!-- Header with buttons -->
      <div class="flex items-center justify-between px-4 py-2 border-b">
        <Button variant="ghost" size="icon" class="h-6 w-6" onclick={onClose}>
          <div class="flex items-center">
            <ChevronRight class="h-3 w-3 -mr-3" />
            <ChevronRight class="h-3 w-3" />
          </div>
        </Button>
        
        <!-- Footer content moved to header right -->
        <div class="flex items-center gap-2">
          <slot name="footer" />
        </div>
      </div>
      
      <!-- Content area -->
      <div class="flex-1 overflow-y-auto scrollbar-none">
        <div class="p-6">
          <slot />
        </div>
      </div>
    </div>
  </div>
</div>
{/if}
