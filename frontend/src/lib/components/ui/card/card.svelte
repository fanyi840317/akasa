<script lang="ts">
    import { cn } from "$lib/utils";
    import type { Snippet } from "svelte";
  
    let {
      class: className = "",
      children,
      ...restProps
    } = $props<{
      children: Snippet;
      class?: string;
    }>();
  </script>
 <div
 class={cn(
   "rounded-xl flex flex-col items-center justify-center overflow-hidden transition-all duration-150 cursor-pointer select-none",
   "bg-base-300 border border-white/5 shadow-2xl outline-1 outline-black/5 p-2",
   className
 )}
 {...restProps}
>
 {@render children?.()}
</div>
  