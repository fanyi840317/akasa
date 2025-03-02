<script lang="ts">
  import { cn } from "$lib/utils";
  import { Button } from "$lib/components/ui/button";
  import { Card } from "$lib/components/ui/card";
  import { ChevronRight, ChevronLeft, X } from "lucide-svelte";
  import { fade, fly } from 'svelte/transition';

  export let steps: { title: string; description: string }[] = [];
  export let currentStep = 0;
  export let onStepChange: (step: number) => void = () => {};
  export let closeWind: any;

  $: totalSteps = steps.length;

  function nextStep() {
    if (currentStep < totalSteps - 1) {
      currentStep++;
      onStepChange(currentStep);
    }
  }

  function prevStep() {
    if (currentStep > 0) {
      currentStep--;
      onStepChange(currentStep);
    }
  }
</script>

{#if true}
<div transition:fade={{ duration: 200 }}>
  <div class="w-full h-screen max-w-none m-0 fixed top-0 left-0 bg-background/95 backdrop-blur-sm z-[1000]" transition:fly={{ y: 20, duration: 300 }}>
    <div class="flex items-center justify-between px-6 py-4 border-b">
      <h2 class="text-lg font-semibold">{steps[currentStep]?.title || ''}</h2>
      <Button variant="ghost" size="icon" class="-mr-2" onclick={closeWind}>
        <X class="h-4 w-4" />
      </Button>
    </div>
    <div class="flex h-[calc(100vh-4rem)]">
      <!-- 左侧步骤导航 -->
      <div class="w-64 p-6 border-r bg-muted/50">
        {#each steps as step, index}
          <div
            class={cn(
              "flex items-start mb-6 last:mb-0 opacity-50",
              index === currentStep && "opacity-100",
              index < currentStep && "opacity-70"
            )}
          >
            <div class={cn(
              "flex items-center justify-center w-8 h-8 rounded-full bg-muted text-muted-foreground font-medium mr-3 shrink-0",
              index === currentStep && "bg-primary text-primary-foreground",
              index < currentStep && "bg-primary/70 text-primary-foreground"
            )}>{index + 1}</div>
            <div class="flex-1">
              <h3 class="text-sm font-medium mb-1">{step.title}</h3>
              <p class="text-xs text-muted-foreground">{step.description}</p>
            </div>
          </div>
        {/each}
      </div>

      <!-- 右侧内容区域 -->
      <div class="flex-1 p-6 flex flex-col">
        <div class="flex-1">
          <slot />
        </div>

        <!-- 导航按钮 -->
        <div class="flex justify-between mt-6">
          {#if currentStep > 0}
            <Button variant="outline" onclick={prevStep}>
              <ChevronLeft class="mr-2 h-4 w-4" />
              上一步
            </Button>
          {/if}

          {#if currentStep < totalSteps - 1}
            <Button onclick={nextStep}>
              下一步
              <ChevronRight class="ml-2 h-4 w-4" />
            </Button>
          {/if}
        </div>
      </div>
    </div>
  </div>
</div>
{/if}