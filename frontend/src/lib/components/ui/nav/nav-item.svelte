<script lang="ts">
  import type { ComponentType } from "svelte";
  import { cn } from "$lib/utils";

  let {
    href,
    icon,
    label,
    isActive = false,
    iconClass = "",
    class: className = "",
    ...restProps
  } = $props<{
    href: string;
    icon: ComponentType;
    label: string;
    isActive?: boolean;
    iconClass?: string;
    class?: string;
  }>();
</script>

<li>
  <a
    {href}
    class={cn(
      "btn btn-secondary text-base-content/50 btn-ghost justify-start",
      "hover:btn-neutral hover:border-base-200",
      isActive && "btn-active text-base-content",
      className
    )}
    {...restProps}
  >
    <!-- svelte-ignore svelte_component_deprecated -->
    <svelte:component
      this={icon}
      class={cn("w-4 h-4", iconClass)}
    />
    {label}
  </a>
</li>