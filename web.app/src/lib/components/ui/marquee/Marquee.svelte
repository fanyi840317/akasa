<script lang="ts">
  import { onMount } from 'svelte';

  export let pauseOnHover = false;
  export let reverse = false;
  export let className = '';

  let containerRef: HTMLDivElement;
  let animationElements: HTMLElement[] = [];

  // 更新动画状态
  function updateAnimationState() {
    if (!containerRef) return;

    animationElements.forEach(el => {
      el.style.animationPlayState = pauseOnHover ? 'paused' : 'running';
    });
  }

  onMount(() => {
    if (containerRef) {
      animationElements = Array.from(
        containerRef.querySelectorAll('.animate-marquee, .animate-marquee-reverse')
      ) as HTMLElement[];

      updateAnimationState();
    }

    return () => {
      animationElements = [];
    };
  });

  // 监听pauseOnHover变化
  $: if (pauseOnHover !== undefined && containerRef) {
    updateAnimationState();
  }
</script>

<div
  bind:this={containerRef}
  class="group flex w-full overflow-hidden {className}"
>
  <div
    class="flex min-w-full shrink-0 items-center justify-around gap-4 py-4"
    class:animate-marquee={!reverse}
    class:animate-marquee-reverse={reverse}
  >
    <slot />
  </div>
  <div
    class="flex min-w-full shrink-0 items-center justify-around gap-4 py-4"
    class:animate-marquee={!reverse}
    class:animate-marquee-reverse={reverse}
  >
    <slot />
  </div>
</div>

<style>
  @keyframes marquee {
    0% {
      transform: translateX(0%);
    }
    100% {
      transform: translateX(-100%);
    }
  }

  @keyframes marquee-reverse {
    0% {
      transform: translateX(-100%);
    }
    100% {
      transform: translateX(0%);
    }
  }

  .animate-marquee {
    animation: marquee var(--duration, 30s) linear infinite;
  }

  .animate-marquee-reverse {
    animation: marquee-reverse var(--duration, 30s) linear infinite;
  }
</style>
