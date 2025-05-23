<script lang="ts">
  import { cn } from "$lib/utils";
  import type { Snippet } from "svelte";

  let {
    class: className = "",
    children,
    rightContent,
    ...restProps
  } = $props<{
    children: Snippet;
    class?: string;
    rightContent?: Snippet;
  }>();
</script>

<div class={cn("relative flex felx-row items-center gap-1",
   "hover:shadow-xl  hover:scale-105 active:scale-95",
   "text-base-content/50 hover:text-base-content",
   className
  
)} {...restProps}>
  <div
    class={cn(
      "rounded-lg flex items-center justify-center overflow-hidden transition-all duration-150 cursor-pointer select-none",
      "bg-base-300 border border-white/5 shadow-2xl outline-1 outline-black/5",
      "w-[62px] h-[36px]",
      className
    )}
    {...restProps}
  >
    {@render children?.()}
  </div>
  {@render rightContent?.()}
</div>
