<script lang="ts">
  import { onMount } from "svelte";
  import { fade, fly } from "svelte/transition";
  import { cn } from "$lib/utils";

  // 定义组件属性
  let {
    texts = [], // 要轮播的文本数组
    interval = 5000, // 轮播间隔，默认5秒
    class: className = "", // 自定义类名
    ghost = false, // ghost模式，只显示文字，不显示导航点和按钮
  } = $props();

  let currentIndex = $state(0);
  let isTransitioning = $state(false);

  // 自动轮播
  onMount(() => {
    const timer = setInterval(() => {
      nextSlide();
    }, interval);

    return () => {
      clearInterval(timer);
    };
  });

  // 切换到下一张幻灯片
  function nextSlide() {
    if (isTransitioning || texts.length <= 1) return;
    
    isTransitioning = true;
    setTimeout(() => {
      currentIndex = (currentIndex + 1) % texts.length;
      isTransitioning = false;
    }, 500); // 500ms是过渡动画的时间
  }

  // 切换到上一张幻灯片
  function prevSlide() {
    if (isTransitioning || texts.length <= 1) return;
    
    isTransitioning = true;
    setTimeout(() => {
      currentIndex = (currentIndex - 1 + texts.length) % texts.length;
      isTransitioning = false;
    }, 500);
  }
</script>

<div class={cn(
  "relative overflow-hidden w-full", 
  !ghost && "rounded-lg bg-base-100 shadow-md", 
  className
)}>
  <div class="carousel-container relative w-full h-full">
    {#each texts as text, i}
      {#if i === currentIndex}
        <div 
          class="carousel-item absolute w-full h-full flex items-center justify-center text-center px-4"
          in:fly={{ y: ghost ? 10 : 20, duration: ghost ? 300 : 500, delay: ghost ? 50 : 100 }}
          out:fade={{ duration: ghost ? 200 : 300 }}
        >
          <p class={cn(
            "font-medium", 
            ghost ? "text-base md:text-lg text-base-content/80" : "text-lg md:text-xl"
          )}>{text}</p>
        </div>
      {/if}
    {/each}
  </div>
  
  <!-- 导航点 - 仅在非ghost模式下显示 -->
  {#if !ghost}
    <div class="absolute bottom-2 left-0 right-0 flex justify-center gap-2">
      {#each texts as _, i}
        <button 
          class="w-2 h-2 rounded-full transition-all duration-300 focus:outline-none"
          class:bg-primary={i === currentIndex}
          class:bg-base-300={i !== currentIndex}
          aria-label={`Go to slide ${i + 1}`}
          on:click={() => {
            if (!isTransitioning) {
              isTransitioning = true;
              setTimeout(() => {
                currentIndex = i;
                isTransitioning = false;
              }, 500);
            }
          }}
        ></button>
      {/each}
    </div>
  
    <!-- 左右导航按钮 - 仅在非ghost模式且有多个文本时显示 -->
    {#if texts.length > 1}
      <button 
        class="absolute left-2 top-1/2 -translate-y-1/2 w-8 h-8 rounded-full bg-base-100/70 flex items-center justify-center hover:bg-base-100 transition-colors"
        aria-label="Previous slide"
        on:click={prevSlide}
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M15 18l-6-6 6-6"/>
        </svg>
      </button>
      <button 
        class="absolute right-2 top-1/2 -translate-y-1/2 w-8 h-8 rounded-full bg-base-100/70 flex items-center justify-center hover:bg-base-100 transition-colors"
        aria-label="Next slide"
        on:click={nextSlide}
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M9 18l6-6-6-6"/>
        </svg>
      </button>
    {/if}
  {/if}
</div>

<style>
  .carousel-container {
    height: 120px; /* 设置固定高度，可以根据需要调整 */
  }
  
  .carousel-item {
    opacity: 1;
    transition: opacity 0.5s ease;
  }
</style>