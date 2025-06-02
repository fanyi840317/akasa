<script lang="ts">
  import type { Snippet } from "svelte";
  import { cn } from "$lib/utils";
  import InfoCard from "$lib/components/ui/card/info-card.svelte";
  import { fade } from "svelte/transition";

  let {
    content,
    position = "bottom",
    class: className = "",
    tooltipClass = "",
    children,
    useInfoCard = false,
    title,
    description,
    info,
    size = "xs",
    contentClass = "",
  } = $props<{
    content?: string | Snippet | null;
    position?: "top" | "bottom" | "left" | "right";
    class?: string;
    tooltipClass?: string;
    children: Snippet;
    useInfoCard?: boolean;
    title?: string;
    description?: string;
    info?: string;
    size?: "xs" | "sm";
    contentClass?: string;
  }>();

  const positionClass =
    position === "top"
      ? "tooltip-top"
      : position === "bottom"
        ? "tooltip-bottom"
        : position === "left"
          ? "tooltip-left"
          : "tooltip-right";
</script>

<div class={cn("tooltip", className, positionClass)}>
  {#if typeof content === "string"}
    <div
      class="tooltip-content text-base-content bg-base-300 rounded-lg p-2 text-xs {tooltipClass}"
    >
      {@html content}
    </div>
  {:else}
    <div
      class="tooltip-content bg-base-300 rounded-lg p-2 text-xs {tooltipClass}"
    >
      {@render content()}
    </div>
  {/if}
  {@render children()}
</div>
