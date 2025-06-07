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
    "btn border border-border px-4 py-2 btn-sm",
    "bg-base-200/80 hover:bg-base-200",
    "text-base-content/70 hover:text-base-content",
    "transition-all duration-200 hover:shadow-sm",
    className,
  )}
  {...restProps}
>
{@render children?.()}
</button>
