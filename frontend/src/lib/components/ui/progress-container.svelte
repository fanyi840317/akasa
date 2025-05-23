<script lang="ts">
  import type { Snippet } from "svelte";
  import { cn } from "$lib/utils";

  let {
    class: className = "",
    progress,
    children,
    size,
  }: {
    class?: string;
    progress?: number | null;
    children?: Snippet;
    size?: "xxs" | "xs" | "sm" | "md" | "lg"; // Add specific types for size
  } = $props();

  // Map size prop to daisyUI loading classes
  const loadingSizeClass =
    size === "xxs"
      ? "loading-xs"
      : size === "xs"
        ? "loading-xs"
        : size === "sm"
          ? "loading-sm"
          : size === "md"
            ? "loading-md"
            : size === "lg"
              ? "loading-lg"
              : "loading-md"; // Default to md if size is not specified or recognized

  // Map size prop to radial progress CSS variables
  const radialProgressStyles = (() => {
    switch (size) {
      case "xxs":
        return "--size:1.5rem; --thickness: 1px;";
      case "xs":
        return "--size:2rem; --thickness: 1px;";
      case "sm":
        return "--size:4rem; --thickness: 2px;";
      case "md":
        return "--size:8rem; --thickness: 4px;";
      case "lg":
        return "--size:12rem; --thickness: 6px;";
      default:
        return "--size:8rem; --thickness: 4px;"; // Default to md
    }
  })();

  // Map size prop to font size classes
  const fontSizeClass =
    size === "xxs"
      ? "text-[8px]"
      : size === "xs"
        ? "text-xs"
        : size === "sm"
          ? "text-sm"
          : size === "md"
            ? "text-base"
            : size === "lg"
              ? "text-lg"
              : "text-base"; // Default to base if size is not specified or recognized
</script>

<div
  class={cn(
    "relative w-full h-full flex items-center justify-center",
    className
  )}
>
  {#if progress !== undefined && progress !== null && progress >= 0 && progress <= 100}
    <div
      class={cn("radial-progress bg-primary text-primary-content border-primary border-4", fontSizeClass)}
      style="--value:{progress}; {radialProgressStyles}"
      aria-valuenow={progress}
      role="progressbar"
    >
      {progress}%
    </div>
  {:else if children}
    {@render children()}
  {:else}
    <span class={cn("loading loading-ring text-primary", loadingSizeClass)}
    ></span>
  {/if}
</div>
