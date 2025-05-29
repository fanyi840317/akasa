<script lang="ts">
  import type { ComponentType } from "svelte";
  import { cn } from "$lib/utils";

  let {
    href,
    icon,
    label,
    color,
    isActive = false,
    class: className = "",
    ...restProps
  } = $props<{
    href: string;
    icon: ComponentType;
    label: string;
    color: string;
    isActive?: boolean;
    class?: string;
  }>();
</script>

<li>
  <a
    {href}
    class={cn(
      "btn btn-secondary text-base-content/50 btn-ghost justify-start",
      isActive && "btn-active",
      className
    )}
    {...restProps}
  >
    <!-- svelte-ignore svelte_component_deprecated -->
    <svelte:component
      this={icon}
      class={cn(
        "w-3 h-3 mr-1 p-0.5 rounded-sm text-base-content/50",
        color
      )}
    />
    {label}
  </a>
</li>