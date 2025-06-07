<script lang="ts">
    import { cn } from "$lib/utils";
  
    let {
      onClick = undefined,
      class: className = "",
      children,
      ...restProps
    } = $props<{
      onClick?: () => void;
      class?: string;
      [key: string]: any;
    }>();
  </script>
  
  <button
    class={cn(
      "flex items-center justify-center",
      "cursor-pointer",
      "size-6 rounded-md border border-base-300/70",
      "bg-base-200/80 hover:bg-base-200",
      "text-base-content/70 hover:text-base-content",
      "transition-all duration-200 hover:shadow-sm",
      className
    )}
    onclick={onClick}
    {...restProps}
  >
    {@render children?.()}
  </button>
  