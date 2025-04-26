<script lang="ts">
  export let pauseOnHover = false;
  export let reverse = false;
  export let className = '';
</script>

<div
  class="group flex w-full overflow-hidden {className}"
  class:hover:[animation-play-state:paused]={pauseOnHover}
>
  <div
    class="flex min-w-full shrink-0 animate-marquee items-center justify-around gap-4 py-4"
    class:animate-marquee={!reverse}
    class:animate-marquee-reverse={reverse}
  >
    <slot />
  </div>
  <div
    class="flex min-w-full shrink-0 animate-marquee items-center justify-around gap-4 py-4"
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
