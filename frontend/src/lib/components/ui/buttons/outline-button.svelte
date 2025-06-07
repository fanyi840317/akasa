<script lang="ts">
    import { cn } from "$lib/utils";
  
    let {
      class: className = "",
      children,
      ...restProps
    } = $props<{
      class?: string;
      [key: string]: any;
    }>();
  </script>
  
  <button
    class={cn(
      "flex items-center justify-center",
      "cursor-pointer",
      "size-6 rounded-xl text-sm px-4 py-4 border border-border",
      "bg-base-200/80 hover:bg-base-200",
      "text-base-content/70 hover:text-base-content",
      "transition-all duration-200 hover:shadow-sm",
      className
    )}
    {...restProps}
  >
  <div class="flex items-center justify-center ">
    {@render children?.()}</div>
  </button>
  