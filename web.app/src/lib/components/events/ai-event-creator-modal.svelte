<script lang="ts">
  import { createEventDispatcher, onMount } from "svelte";
  import { Button } from "$lib/components/ui/button";
  import { ScrollArea } from "$lib/components/ui/scroll-area";
  import { Textarea } from "$lib/components/ui/textarea";
  import { Loader2, ArrowLeft, Send } from "lucide-svelte";
  import { aiService } from "$lib/services/ai";
  import { PUBLIC_GEMINI_API_KEY } from "$env/static/public";
  import Modal from "$lib/components/ui/modal/modal.svelte";
  import AiGeneratingStatus from "$lib/components/ai/ai-generating-status.svelte";
  import X from "@lucide/svelte/icons/x";
  import { DividerBlockMarkdownAdapterExtension } from "@blocksuite/blocks";
  import { marked } from "marked";
  import { sleep } from "@blocksuite/global/utils";
  import { MapBase } from "$lib/components/map";
  import { fade, fly, slide } from "svelte/transition";
  import { quintOut } from "svelte/easing";
  import { cn } from "$lib/utils"; // Import cn utility

  let { open = $bindable(false) } = $props<{ open: boolean }>();

  const dispatch = createEventDispatcher();

  let eventInput = $state("");
  let generatedTitle = $state("");
  let generatedContent = $state("");
  let generatedEventTime = $state<string | undefined>(undefined); // 新增：存储事件时间
  let generatedEntities = $state<{
    people?: Array<{ name: string; role: string }>;
    locations?: Array<{ name: string; description: string; coordinates?: [number, number] }>;
    timeline?: Array<{ time: string; event: string }>;
  }>({});
  let displayedTitle = $state("");
  let displayedContent = $state("");
  let isLoading = $state(false);
  let isSaving = $state(false); // Add saving state
  let selectedLocationIndex = $state<number | null>(null); // Add state for selected location index
  let error = $state<string | null>(null);
  let mode: "input" | "loading" | "result" = $state("input");
  let typingInterval: ReturnType<typeof setInterval> | null = null;

  // 跟踪AI生成过程的步骤
  // 0: 生成标题, 1: 生成内容, 2: 提取实体, 3: 生成时间线, 4: 生成图谱
  let generationStep = $state(0);
  let animationCompleted = $state(false); // 跟踪左侧动画是否完成

  let contentContainer = $state<HTMLDivElement | null>(null);
  let scrollAreaRef = $state<HTMLDivElement | null>(null);
  let textareaElement = $state<HTMLTextAreaElement | null>(null);

  async function generateFromInput() {
    if (!eventInput) {
      error = "请输入事件名称、链接或您的经历。";
      return;
    }
    error = null;
    isLoading = true;
    mode = "loading";
    generatedTitle = "";
    generatedContent = "";
    displayedTitle = "";
    displayedContent = "";

    // 重置生成步骤
    generationStep = 0;

    try {
      // 获取AI生成的内容
      const result = await aiService.generateEventContent({
        apiKey: PUBLIC_GEMINI_API_KEY,
        description: eventInput,
      });
      generationStep = 1;

      // 存储事件时间
      generatedEventTime = result.eventTime;

      // 检查是否需要额外解析
      if (
        result.content &&
        result.content.startsWith("{") &&
        result.content.includes('"title"') &&
        result.content.includes('"content"')
      ) {
        try {
          // 尝试解析 content 中的 JSON
          const parsedContent = JSON.parse(result.content);
          if (parsedContent.title && parsedContent.content) {
            generatedTitle = parsedContent.title;
            generatedContent = parsedContent.content;
            generatedEntities = parsedContent.entities || {};
            generatedEventTime = parsedContent.eventTime || result.eventTime; // 优先使用解析出的，否则用原始的
            console.log("成功从 content 中解析出 JSON 数据", {
              generatedTitle,
              generatedContent,
              generatedEntities,
            });
          } else {
            // 如果解析出的 JSON 不包含需要的字段，使用原始数据
            generatedTitle = result.title;
            generatedContent = result.content;
            generatedEntities = result.entities || {};
            generatedEventTime = result.eventTime;
          }
        } catch (e) {
          console.error("解析 content 中的 JSON 失败", e);
          // 解析失败，使用原始数据
          generatedTitle = result.title;
          generatedContent = result.content;
          generatedEntities = result.entities || {};
        }
      } else {
        // 使用原始数据
        generatedTitle = result.title;
        generatedContent = result.content;
        generatedEntities = result.entities || {};
      }

      // 直接设置最终步骤，让 AiGeneratingStatus 组件自动处理动画
      // 设置最终步骤为4（生成图谱）
      generationStep = 4;
    } catch (err: any) {
      console.error("AI 生成失败:", err);
      const errorMessage = err instanceof Error ? err.message : String(err);
      error = `无法生成内容：${errorMessage}`;
      mode = "input";
      generationStep = 0;
    } finally {
      // isLoading 状态保持，直到所有动画完成
      // 在 startTypewriterEffect 中设置 isLoading = false
    }
  }

  function startTypewriterEffect() {
    // 确保动画已完成
    if (!animationCompleted) {
      console.warn("尝试在动画完成前启动打字机效果");
      return;
    }

    mode = "result";
    let titleIndex = 0;
    let contentIndex = 0;
    let isTypingTitle = true;

    // 清除之前的打字机效果
    if (typingInterval) {
      clearInterval(typingInterval);
    }

    typingInterval = setInterval(() => {
      if (isTypingTitle) {
        if (titleIndex < generatedTitle.length) {
          displayedTitle = generatedTitle.substring(0, titleIndex + 1);
          titleIndex++;
        } else {
          isTypingTitle = false;
        }
      } else {
        if (contentIndex < generatedContent.length) {
          // 一次添加多个字符，使打字效果更自然
          const charsToAdd = Math.min(
            5,
            generatedContent.length - contentIndex,
          ); // 每次添加最多5个字符
          contentIndex += charsToAdd;
          displayedContent = generatedContent.substring(0, contentIndex);

          // 不在打字机效果中处理滚动，而是依赖 $effect 来处理
        } else {
          // 打字效果完成
          if (typingInterval) {
            clearInterval(typingInterval);
            typingInterval = null;
          }
          isLoading = false;
          // Automatically select the first location with coordinates if only one exists
          const locationsWithCoords = generatedEntities.locations?.filter(l => l.coordinates);
          if (locationsWithCoords?.length === 1) {
            selectedLocationIndex = generatedEntities.locations?.findIndex(l => l.coordinates) ?? null;
          }
        }
      }
    }, 20); // 调整为适中的打字速度，平衡效果和速度
  }

  async function handleSave() {
    if (isSaving) return;

    // Check if selection is required
    const locationsWithCoords = generatedEntities.locations?.filter(l => l.coordinates);
    if (locationsWithCoords && locationsWithCoords.length > 1 && selectedLocationIndex === null) {
      error = "请选择一个主要事件地点。";
      return;
    }
    error = null;
    isSaving = true;

    let primaryLocation = null;
    if (selectedLocationIndex !== null && generatedEntities.locations) {
      primaryLocation = generatedEntities.locations[selectedLocationIndex];
    }

    // Simulate saving delay
    await sleep(500);

    dispatch("save", {
      title: generatedTitle,
      content: generatedContent,
      eventTime: generatedEventTime,
      entities: generatedEntities,
      primaryLocation: primaryLocation, // Add selected primary location
    });

    isSaving = false;
    closeModalAndReset();
  }

  function handleBack() {
    mode = "input";
    error = null;
  }

  function handleClose() {
    closeModalAndReset();
    dispatch("close");
  }

  function closeModalAndReset() {
    // 清除打字机效果
    if (typingInterval) {
      clearInterval(typingInterval);
      typingInterval = null;
    }

    open = false;
    setTimeout(() => {
      resetState();
    }, 300);
  }

  function resetState() {
    eventInput = "";
    generatedTitle = "";
    generatedContent = "";
    generatedEventTime = undefined; // 重置事件时间
    generatedEntities = {};
    displayedTitle = "";
    displayedContent = "";
    isLoading = false;
    isSaving = false; // Reset saving state
    selectedLocationIndex = null; // Reset selected location
    error = null;
    mode = "input";
    generationStep = 0;
    animationCompleted = false; // 重置动画完成状态
  }

  // 监听 displayedContent 变化，始终保持滚动条在底部
  $effect(() => {
    if (displayedContent && mode === "result" && scrollAreaRef) {

      // 使用 requestAnimationFrame 确保在渲染周期中执行滚动
      requestAnimationFrame(() => {
        try {
          // 查找 viewport 元素 - 这是最可靠的滚动元素
          const viewport = scrollAreaRef?.querySelector(
            "[data-scroll-area-viewport]",
          );
          if (viewport) {
            // 始终立即滚动到底部，确保用户看到最新内容
            viewport.scrollTop = viewport.scrollHeight;
          }
        } catch (e) {
          console.error("滚动失败:", e);
        }
      });
    }
  });

  // 自动调整文本框高度的函数
  function autoResizeTextarea(_: Event) {
    if (!textareaElement) return;

    // 重置高度，以便正确计算新的高度
    textareaElement.style.height = "auto";

    // 设置新的高度 - scrollHeight 是内容的实际高度
    const newHeight = Math.min(
      300,
      Math.max(100, textareaElement.scrollHeight),
    );
    textareaElement.style.height = `${newHeight}px`;
  }

  // 组件卸载时清除定时器
  onMount(() => {
    // 初始化文本框高度
    if (textareaElement) {
      autoResizeTextarea(new Event("input"));
    }

    return () => {
      if (typingInterval) {
        clearInterval(typingInterval);
      }
    };
  });
</script>

<Modal bind:open class="h-[75vh] w-[75vw] max-w-[960px]">
  <!-- Header -->
  <div class="absolute top-2 left-2 z-10">
    {#if mode === "input"}
      <Button
        size="icon"
        variant="ghost"
        class="p-1 rounded-full"
        onclick={handleClose}
        aria-label="关闭"
      >
        <X class="h-4 w-4" />
      </Button>
    {:else}
      <Button
        size="icon"
        variant="ghost"
        class="p-1 rounded-full"
        onclick={handleBack}
        aria-label="返回"
      >
        <ArrowLeft class="h-4 w-4" />
      </Button>
    {/if}
  </div>

  <!-- Content -->
  {#if mode === "input"}
    <div
      class="flex-grow flex flex-col items-center justify-center w-full h-full"
    >
      <!-- <div
        class=" w-20 h-20 bg-neutral-200/90 dark:bg-neutral-800 rounded-full flex items-center justify-center mb-4"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="text-neutral-400"
          ><path
            d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"
          /></svg
        >
      </div> -->
      <h2 class="text-2xl font-bold mb-6">您想写点关于什么的内容？</h2>
      <div class="w-[70%] max-w-3xl mx-auto relative">
        <div
          class="relative border border-neutral-300 dark:border-neutral-700 rounded-xl shadow-sm bg-white dark:bg-neutral-800 overflow-hidden"
        >
          <textarea
            class="min-h-[100px] max-h-[300px] py-4 px-4 pr-12 w-full resize-none bg-transparent border-none focus:ring-0 focus:outline-none placeholder:text-neutral-500/70 overflow-hidden"
            bind:value={eventInput}
            bind:this={textareaElement}
            placeholder="输入事件名称、填入链接或您的经历..."
            oninput={autoResizeTextarea}
          ></textarea>
          <div class="absolute bottom-2 right-4 flex items-center">
            <Button
              size="icon"
              onclick={generateFromInput}
              class="rounded-full p-2 shadow-md transition-colors
              disabled:opacity-50 disabled:cursor-not-allowed"
              disabled={isLoading || !eventInput}
            >
              <Send class="h-5 w-5" strokeWidth={3}></Send>
            </Button>
          </div>
        </div>
      </div>

      {#if error}
        <p class="text-red-400 mt-4">{error}</p>
      {/if}
    </div>
  {:else if mode === "loading" || mode === "result"}
    <div class="flex flex-row w-full h-[calc(75vh-10px)] p-4">
      <!-- 左侧：生成状态或实体信息卡片 -->
      {#if mode === "loading" || (mode === "result" && !animationCompleted)}
        <!-- 在生成过程中显示生成状态 -->
        <div
          class="w-1/3 flex flex-col h-full justify-between"
          in:fade={{ duration: 300 }}
          out:fade={{ duration: 200 }}
        >
          <div class="my-6">
            <AiGeneratingStatus
              bind:requestedStep={generationStep}
              onComplete={() => {
                animationCompleted = true;
                startTypewriterEffect();
              }}
            />
          </div>

        </div>
      {:else if mode === "result" && animationCompleted && (generatedEntities.people?.length || generatedEntities.locations?.length || generatedEntities.timeline?.length)}
        <!-- 在生成完成后显示实体信息卡片 -->
        <div
          class="w-1/3 flex flex-col h-full justify-between mt-6 "
          in:fly={{ x: -20, duration: 400, delay: 200, easing: quintOut }}
          out:fade={{ duration: 200 }}
        >
          <ScrollArea class="flex-1 max-h-[calc(75vh-120px)] pr-2">
            <div class="space-y-6 p-2">

            <!-- 事件时间 -->
            {#if generatedEventTime}
              <div>
                <h3 class="text-lg font-bold text-white mb-4">
                  事件时间
                </h3>
                <div class="grid grid-cols-1 gap-3">
                  <div
                    class="bg-neutral-800 rounded-md shadow-md border border-neutral-700 overflow-hidden transform transition-all hover:shadow-lg"
                    in:fly={{ y: 10, x: 0, duration: 300, delay: 300 }}
                  >
                    <div class="flex items-center p-3">
                      <div
                        class="w-8 h-8 rounded-full bg-neutral-700 flex items-center justify-center text-sm font-bold mr-3 flex-shrink-0"
                      >
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          class="h-4 w-4"
                          viewBox="0 0 24 24"
                          fill="none"
                          stroke="currentColor"
                          stroke-width="2"
                          stroke-linecap="round"
                          stroke-linejoin="round"
                        >
                          <rect width="18" height="18" x="3" y="4" rx="2" ry="2" />
                          <line x1="16" x2="16" y1="2" y2="6" />
                          <line x1="8" x2="8" y1="2" y2="6" />
                          <line x1="3" x2="21" y1="10" y2="10" />
                        </svg>
                      </div>
                      <div class="flex-1 min-w-0">
                        <div class="text-sm font-medium text-white truncate">
                          {generatedEventTime}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            {/if}

            <!-- 人物信息 -->
            {#if generatedEntities.people?.length}
              <div>
                <h3 class="text-lg font-bold text-white mb-4">
                  相关人物
                </h3>
                <div class="grid grid-cols-1 gap-3">
                  {#each generatedEntities.people as person, index}
                    <div
                      class="bg-neutral-800 rounded-md shadow-md border border-neutral-700 overflow-hidden transform transition-all hover:shadow-lg"
                      in:fly={{ y: 10, x: 0, duration: 300, delay: 300 + index * 100 }}
                    >
                      <div class="flex items-center p-3">
                        <div
                          class="w-8 h-8 rounded-full bg-neutral-700 flex items-center justify-center text-sm font-bold mr-3 flex-shrink-0"
                        >
                          {person.name[0] || "?"}
                        </div>
                        <div class="flex-1 min-w-0">
                          <div class="text-sm font-medium text-white truncate">
                            {person.name}
                          </div>
                          <div class="text-xs text-neutral-400 truncate">
                            {person.role}
                          </div>
                        </div>
                      </div>
                    </div>
                  {/each}
                </div>
              </div>
            {/if}

            <!-- 地点信息 -->
            {#if generatedEntities.locations?.length}
              <div>
                <h3 class="text-lg font-bold text-white mb-4">
                  相关地点 {#if (generatedEntities.locations?.filter(l => l.coordinates)?.length || 0) > 1}
                    <span class="text-sm font-normal text-neutral-400">(请选择主要地点)</span>
                  {/if}
                </h3>
                <div class="grid grid-cols-1 gap-3">
                  {#each generatedEntities.locations as location, index}
                    {@const hasCoordinates = !!location.coordinates}
                    {@const isSelected = selectedLocationIndex === index}
                    <div
                      class={cn(
                        "bg-neutral-800 rounded-md shadow-md border border-neutral-700 overflow-hidden transform transition-all hover:shadow-lg",
                        hasCoordinates && "cursor-pointer hover:border-blue-500",
                        isSelected && "border-2 border-blue-500 ring-2 ring-blue-500/50"
                      )}
                      in:fly={{ y: 10, x: 0, duration: 300, delay: 500 + index * 100 }}
                      onclick={() => {
                        if (hasCoordinates) {
                          selectedLocationIndex = index;
                          error = null; // Clear error on selection
                        }
                      }}
                      role={hasCoordinates ? "button" : undefined}
                      tabindex={hasCoordinates ? 0 : -1}
                      aria-pressed={isSelected}
                    >
                      <!-- 如果有坐标，显示地图 -->
                      {#if location.coordinates}
                        <div class="w-full h-24 relative pointer-events-none"> <!-- Disable map interaction -->
                          <MapBase
                            locationData={{
                              latitude: location.coordinates[0],
                              longitude: location.coordinates[1]
                            }}
                            zoom={11}
                            showUserLocation={false}
                            showLocateButton={false}
                            clickable={false}
                          />
                        </div>
                      {/if}

                      <div class="flex items-center p-3">
                        <div
                          class="w-8 h-8 rounded-full bg-neutral-900 flex items-center justify-center text-sm font-bold mr-3 flex-shrink-0"
                        >
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            class="h-4 w-4"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="2"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                          >
                            <path
                              d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"
                            ></path>
                            <circle cx="12" cy="10" r="3"></circle>
                          </svg>
                        </div>
                        <div class="flex-1 min-w-0">
                          <div class="text-sm font-medium text-white truncate">
                            {location.name}
                            {#if isSelected}
                              <span class="ml-2 text-xs text-blue-400">(已选)</span>
                            {/if}
                          </div>
                          <div class="text-xs text-neutral-400 truncate">
                            {location.description}
                          </div>
                          {#if location.coordinates}
                            <div class="text-xs text-blue-400 mt-1">
                              {location.coordinates[0].toFixed(4)}, {location.coordinates[1].toFixed(4)}
                            </div>
                          {/if}
                        </div>
                      </div>
                    </div>
                  {/each}
                </div>
              </div>
            {/if}

            <!-- 时间线信息 -->
            {#if generatedEntities.timeline?.length}
              <div>
                <h3 class="text-lg font-bold text-white mb-4">
                  时间线
                </h3>
                <div class="grid grid-cols-1 gap-3">
                  {#each generatedEntities.timeline as timepoint, index}
                    <div
                      class="bg-neutral-800 rounded-md shadow-md border border-neutral-700 overflow-hidden transform transition-all hover:shadow-lg"
                      in:fly={{ y: 10, x: 0, duration: 300, delay: 700 + index * 100 }}
                    >
                      <div class="flex items-center p-3">
                        <div
                          class="w-8 h-8 rounded-full bg-neutral-700 flex items-center justify-center text-sm font-bold mr-3 flex-shrink-0"
                        >
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            class="h-4 w-4"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            stroke-width="2"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                          >
                            <circle cx="12" cy="12" r="10"></circle>
                            <polyline points="12 6 12 12 16 14"></polyline>
                          </svg>
                        </div>
                        <div class="flex-1 min-w-0">
                          <div class="text-sm font-medium text-white truncate">
                            {timepoint.time}
                          </div>
                          <div class="text-xs text-neutral-400 truncate">
                            {timepoint.event}
                          </div>
                        </div>
                      </div>
                    </div>
                  {/each}
                </div>
              </div>
            {/if}
            </div>
          </ScrollArea>
          <!-- 保存按钮 -->
          <div class="p-2 mb-4" in:fade={{ duration: 300, delay: 1000 }}>
            <Button
              variant="outline"
              onclick={handleSave}
              class="w-full disabled:opacity-50 disabled:bg-neutral-400 disabled:cursor-not-allowed"
            >
              采用此内容
            </Button>
          </div>
        </div>
      {/if}

      <!-- 生成结果 -->
      <ScrollArea
        bind:ref={scrollAreaRef}
        class="flex-1 w-full bg-neutral-900 rounded-md border border-neutral-800/50"
      >
        <div class="flex flex-col" bind:this={contentContainer}>
          <div class="flex flex-col h-full">
            <div class="p-12 text-white min-h-[60px] items-start">
              {#if mode === "loading"}
                <div
                  class="h-6 w-2/3 bg-neutral-800/50 rounded animate-pulse"
                ></div>
              {:else}
                <h2 class="text-3xl font-bold">
                  {displayedTitle}<span
                    class="animate-caret-blink"
                    class:hidden={displayedTitle === generatedTitle}>|</span>
                  
                </h2>
                {#if mode === "result" && generatedEventTime}
                  <p class="text-sm text-neutral-400 mt-2">{generatedEventTime}</p>
                {/if}
              {/if}
            </div>

            <div class="flex-1 flex flex-row">
              <div class="flex-1 py-6 px-12 whitespace-pre-wrap">
                {#if mode === "loading"}
                  <div class="space-y-2">
                    <div
                      class="h-4 bg-neutral-800/50 rounded animate-pulse"
                    ></div>
                    <div
                      class="h-4 w-5/6 bg-neutral-800/50 rounded animate-pulse"
                    ></div>
                    <div
                      class="h-4 w-4/6 bg-neutral-800/50 rounded animate-pulse"
                    ></div>
                    <div
                      class="h-4 w-2/7 bg-neutral-800/50 rounded animate-pulse"
                    ></div>
                  </div>
                {:else}
                  <div
                    class="prose prose-invert h-full text-left prose-img:rounded-lg prose-img:shadow-lg"
                  >
                    {@html marked(displayedContent)}
                    <span
                      class="animate-caret-blink"
                      class:hidden={displayedContent === generatedContent}
                      >|</span
                    >
                  </div>
                {/if}
              </div>

              <!-- 实体信息卡片已移动到左侧显示，在动画完成后显示 -->
            </div>
          </div>
        </div>
      </ScrollArea>
    </div>
  {/if}
</Modal>

<style lang="postcss">
  :global(.dark) {
    --background: theme(colors.neutral.900);
    --foreground: theme(colors.white);
  }
</style>
