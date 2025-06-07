<script lang="ts">
  import { cn } from "$lib/utils";
  import type { Snippet } from "svelte";

  let {
    class: className = "",
    children,
    content,
    ...restProps
  } = $props<{
    children: Snippet;
    class?: string;
    content?: Snippet;
  }>();
</script>

<div class={cn("relative flex flex-col items-center gap-1",
   "hover:shadow-xl  hover:scale-105 active:scale-95",
   "text-base-content/50 hover:text-base-content", 
   "w-[62px] h-[46px]",
   className
  
)} {...restProps}>
  <div
    class={cn(
      "rounded-lg flex items-center justify-center overflow-hidden transition-all duration-150 cursor-pointer select-none",
      "bg-base-300 border border-white/5 shadow-2xl outline-1 outline-black/5",
      "w-full h-full",
      className
    )}
    {...restProps}
  >
    {@render children?.()}
  </div>
  
  {@render content?.()}
</div>
