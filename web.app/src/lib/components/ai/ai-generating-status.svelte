<script lang="ts">
  import { CheckCircle, Loader, AlertCircle, XCircle } from "lucide-svelte";
  import { onMount, tick, type ComponentProps } from "svelte";
  import { fade, fly } from "svelte/transition";

  // Define step type
  type Step = {
    name: string;
    status: "completed" | "processing" | "pending" | "failed";
    index: number;
  };

  // All possible steps in the AI generation process
  const allSteps: Step[] = [
    { name: "生成标题", status: "pending", index: 0 },
    { name: "生成内容", status: "pending", index: 1 },
    { name: "提取实体", status: "pending", index: 2 },
    { name: "生成时间线", status: "pending", index: 3 },
    { name: "生成图谱", status: "pending", index: 4 },
  ];

  // Current visible steps
  let visibleSteps = $state<Step[]>([]);

  // Allow external control of steps
  let {
    activeStep = $bindable(0),
    requestedStep = $bindable(0),
    onComplete = () => {},
  } = $props<{
    activeStep?: number;
    requestedStep?: number;
    onComplete?: () => void;
  }>();
  let previousRequestedStep = -1;
  let animationInProgress = false;

  // 使用 CSS 动画而不是 JavaScript 定时器

  // Update steps when requestedStep changes
  $effect(() => {
    if (requestedStep !== previousRequestedStep) {
      previousRequestedStep = requestedStep;
      if (!animationInProgress) {
        processNextStep();
      }
    }
  });

  // Initialize with the first step
  onMount(() => {
    // Start with just the first step
    if (requestedStep >= 0) {
      visibleSteps = [{ ...allSteps[0], status: "processing" }];
      // If more steps are requested, process them immediately
      if (requestedStep > 0) {
        processNextStep();
      }
    }
  });

  // Process the next step in the sequence
  async function processNextStep() {
    if (
      animationInProgress ||
      activeStep >= allSteps.length ||
      activeStep >= requestedStep
    ) {
      return;
    }

    animationInProgress = true;

    // 如果是第一个步骤且还没有显示，直接显示它
    if (visibleSteps.length === 0 && requestedStep >= 0) {
      visibleSteps = [{ ...allSteps[0], status: "processing" }];
      await tick();

      // 如果请求的步骤大于0，则立即完成当前步骤
      if (requestedStep > 0) {
        await completeCurrentStep();
        animationInProgress = false;
        processNextStep();
      } else {
        animationInProgress = false;
      }
      return;
    }

    // 如果需要添加一个新步骤
    if (activeStep === visibleSteps.length - 1 && activeStep < requestedStep) {
      // 先完成当前步骤
      await completeCurrentStep();

      // 添加下一个步骤
      const nextStep = allSteps[activeStep];
      // 如果是最后一个步骤（图谱生成），直接设置为完成状态
      const nextStepStatus = nextStep.index === 4 ? "completed" : "processing";

      visibleSteps = [
        ...visibleSteps,
        { ...nextStep, status: nextStepStatus },
      ];
      await tick();

      // 如果还有更多步骤要处理
      if (activeStep < requestedStep) {
        animationInProgress = false;
        processNextStep();
      } else {
        // 所有步骤完成，通知父组件
        animationInProgress = false;
        // 如果是最后一个步骤，调用完成回调
        if (activeStep === allSteps.length - 1) {
          onComplete();
        }
      }
    } else {
      animationInProgress = false;
    }
  }

  // Complete the current step and move to the next one
  async function completeCurrentStep() {
    // Mark the current step as completed
    visibleSteps = visibleSteps.map((step, index) => {
      if (index === activeStep) {
        return { ...step, status: "completed" };
      }
      return step;
    });

    // Update the active step
    activeStep += 1;

    await tick();
    // 使用 await 等待一小段时间，确保动画有时间显示
    await new Promise<void>((resolve) => {
      // 使用 requestAnimationFrame 代替 setTimeout
      requestAnimationFrame(() => {
        requestAnimationFrame(() => resolve());
      });
    });
  }

  function getIcon(status: string) {
    switch (status) {
      case "completed":
        return CheckCircle;
      case "processing":
        return Loader;
      case "failed":
        return XCircle;
      default:
        return Loader; // Use Loader as pending icon but without animation
    }
  }

  function getIconClass(status: string) {
    switch (status) {
      case "completed":
        return "text-gray-400";
      case "processing":
        return "text-blue-500 animate-spin";
      case "failed":
        return "text-red-500";
      default:
        return "text-gray-500 opacity-50";
    }
  }
</script>

<div class="p-6 bg-background rounded-lg w-full max-w-md mx-auto">
  <h3 class="text-lg font-semibold mb-4 text-foreground text-left">
    {#if visibleSteps.length > 0 && visibleSteps.length === allSteps.length && visibleSteps[visibleSteps.length - 1].status === "completed"}
      完成
    {:else if visibleSteps.length === 0}
      正在处理...
    {:else}
      正在{visibleSteps[visibleSteps.length - 1].name}...
    {/if}
  </h3>
  <div class="relative">
    <!-- Multiple line segments connecting steps -->
    {#each visibleSteps as _, i}
      {#if i < visibleSteps.length - 1}
        <div
          class="absolute left-[9px] w-[3px] bg-gray-500/50 z-0"
          style="top: {26 + i * 54}px; height: 28px;"
        ></div>
      {/if}
    {/each}

    <ul class="relative z-10 space-y-8">
      {#each visibleSteps as step (step.index)}
        <li
          class="flex items-center relative"
          in:fly={{ y: 30, duration: 800, delay: 300 }}
          out:fade={{ duration: 300 }}
        >
          <!-- Icon with circle background to cover the line -->
          <div
            class="relative z-20 flex-shrink-0"
            style="width: 24px; height: 24px;"
          >
            <div class="absolute inset-0 bg-background rounded-full -m-1"></div>
            {#if getIcon(step.status) === CheckCircle}
              <CheckCircle
                class="relative h-5 w-5 {getIconClass(step.status)}"
                strokeWidth={step.status === "processing" ? 2.5 : 2}
              />
            {:else if getIcon(step.status) === Loader}
              <Loader
                class="relative h-5 w-5 {getIconClass(step.status)}"
                strokeWidth={step.status === "processing" ? 2.5 : 2}
              />
            {:else if getIcon(step.status) === XCircle}
              <XCircle
                class="relative h-5 w-5 {getIconClass(step.status)}"
                strokeWidth={step.status === "processing" ? 2.5 : 2}
              />
            {/if}
          </div>

          <!-- Step name with colored dots for the "添加属性" step -->
          <span
            class="ml-4 text-sm {step.status === 'processing'
              ? 'text-foreground font-medium'
              : step.status === 'completed'
                ? 'text-gray-400'
                : 'text-gray-500'} flex items-center"
          >
            {step.name}
          </span>
        </li>
      {/each}
    </ul>
  </div>
</div>

<style>
  /* We don't need animations for the simple line style */
</style>
