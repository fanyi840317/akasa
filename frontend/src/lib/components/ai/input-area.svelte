<script lang="ts">
  import { cn } from "$lib/utils";
  import { Globe, Search, User, FileText, Heading, Sparkles, Save } from "lucide-svelte";
  import { toast } from "svelte-sonner";
  import { eventStore } from "$lib/stores/event";
  import { 
    queryRecentMysteriousEvents, 
    extractEntitiesFromMarkdown, 
    generateSummaryFromMarkdown, 
    generateTitleFromMarkdown,
    adoptAIAnalysisToEvent
  } from "$lib/services/aiEnhanced";

  let showSuggestions = false;
  let showAITools = $state(false);
  let rows = $state(2); // 初始行数
  let maxRows = 10; // 最大行数
  let isProcessing = $state(false);

  // 添加属性
  let {
    disabled = false,
    placeholder = "Ask anything",
    inputValue = $bindable(""),
    class:className,
    onSubmit,
    eventMode = false, // 新增：事件模式，用于显示事件相关AI功能
    currentEvent = $bindable(null), // 新增：当前事件，用于自动保存
  } = $props<{
    class?: string;
    disabled?: boolean;
    placeholder?: string;
    inputValue?: string;
    onSubmit?: (text: string) => void;
    eventMode?: boolean;
    currentEvent?: any;
  }>();

  const suggestions = [
    "查询最近一周的神秘事件",
    "从这篇文章中提取人物和地点",
    "为这篇文章生成摘要",
    "为这篇文章生成标题",
  ];

  // 根据内容计算行数
  function calculateRows(text: string): number {
    if (!text) return 2; // 默认至少2行
    
    // 计算换行符数量
    const newLines = (text.match(/\n/g) || []).length;
    
    // 估算每行平均字符数（根据实际情况调整）
    const avgCharsPerLine = 50;
    const textLines = Math.ceil(text.length / avgCharsPerLine);
    
    // 取换行符数量和估算行数的较大值，并确保在2-10行之间
    return Math.max(2, Math.min(maxRows, Math.max(newLines + 1, textLines)));
  }

  // 监听输入值变化，更新行数
  $effect(() => {
    rows = calculateRows(inputValue);
  });

  // 自动保存事件数据
  // $effect(() => {
  //   if (eventMode && currentEvent && inputValue !== currentEvent.content) {
  //     autoSaveEvent();
  //   }
  // });

  // // 自动保存事件数据
  // async function autoSaveEvent() {
  //   if (!eventMode || !currentEvent) return;
    
  //   try {
  //     const updatedEvent = {
  //       ...currentEvent,
  //       content: inputValue
  //     };
      
  //     // 使用事件存储更新事件
  //     await eventStore.updateEvent(updatedEvent.$id,updatedEvent);
  //     console.log('事件内容已自动保存');
  //   } catch (error) {
  //     console.error('自动保存事件失败:', error);
  //   }
  // }

  function handleSubmit() {
    if (inputValue.trim()) {
      onSubmit?.(inputValue.trim());
    }
  }

  function handleSuggestionClick(suggestion: string) {
    inputValue = suggestion;
    showSuggestions = false;
  }

  // 查询最近一周的神秘事件
  async function handleQueryMysteriousEvents() {
    if (isProcessing) return;
    isProcessing = true;
    
    try {
      toast.loading('正在查询最近一周的神秘事件...');
      const events = await queryRecentMysteriousEvents();
      
      // 将结果显示在输入框中
      inputValue = `# 最近一周的神秘事件\n\n${events.map((event, index) => 
        `## ${index + 1}. ${event.title}\n${event.content}\n\n**日期**: ${event.date}\n**地点**: ${event.location_data?.name || '未知'}\n**摘要**: ${event.summary}\n\n---\n\n`
      ).join('')}`;
      
      toast.success('查询成功！');
    } catch (error) {
      console.error('查询神秘事件失败:', error);
      toast.error(`查询失败: ${error instanceof Error ? error.message : '未知错误'}`);
    } finally {
      isProcessing = false;
    }
  }

  // 提取实体
  async function handleExtractEntities() {
    if (!inputValue.trim() || isProcessing) return;
    isProcessing = true;
    
    try {
      toast.loading('正在提取实体...');
      const entitiesJson = await extractEntitiesFromMarkdown(inputValue);
      
      // 将结果添加到输入框末尾
      inputValue += `\n\n## 提取的实体\n\`\`\`json\n${entitiesJson}\n\`\`\`\n`;
      
      toast.success('实体提取成功！');
    } catch (error) {
      console.error('提取实体失败:', error);
      toast.error(`提取失败: ${error instanceof Error ? error.message : '未知错误'}`);
    } finally {
      isProcessing = false;
    }
  }

  // 生成摘要
  async function handleGenerateSummary() {
    if (!inputValue.trim() || isProcessing) return;
    isProcessing = true;
    
    try {
      toast.loading('正在生成摘要...');
      const summary = await generateSummaryFromMarkdown(inputValue);
      
      // 将结果添加到输入框末尾
      inputValue += `\n\n## 摘要\n${summary}\n`;
      
      toast.success('摘要生成成功！');
    } catch (error) {
      console.error('生成摘要失败:', error);
      toast.error(`生成失败: ${error instanceof Error ? error.message : '未知错误'}`);
    } finally {
      isProcessing = false;
    }
  }

  // 生成标题
  async function handleGenerateTitle() {
    if (!inputValue.trim() || isProcessing) return;
    isProcessing = true;
    
    try {
      toast.loading('正在生成标题...');
      const title = await generateTitleFromMarkdown(inputValue);
      
      // 将结果添加到输入框开头
      inputValue = `# ${title}\n\n${inputValue}`;
      
      toast.success('标题生成成功！');
    } catch (error) {
      console.error('生成标题失败:', error);
      toast.error(`生成失败: ${error instanceof Error ? error.message : '未知错误'}`);
    } finally {
      isProcessing = false;
    }
  }

  // 采纳AI分析
  async function handleAdoptAIAnalysis() {
    if (!inputValue.trim() || !currentEvent || isProcessing) return;
    isProcessing = true;
    
    try {
      toast.loading('正在应用AI分析结果...');
      const updatedEvent = await adoptAIAnalysisToEvent(currentEvent, inputValue);
      
      // 更新当前事件
      currentEvent = updatedEvent;
      
      toast.success('AI分析结果已应用到事件！');
    } catch (error) {
      console.error('应用AI分析失败:', error);
      toast.error(`应用失败: ${error instanceof Error ? error.message : '未知错误'}`);
    } finally {
      isProcessing = false;
    }
  }
</script>

<div class={cn("flex-center flex-col",className)}>
  <div class="card bg-base-300 rounded-2xl shadow-sm w-full">
    <div class="card-body p-2 gap-0">
      <!-- 输入框 -->
      <form onsubmit={handleSubmit}>
        <textarea
          rows={rows}
          {placeholder}
          class="p-2 w-full h-full resize-none focus:outline-none bg-transparent"
          bind:value={inputValue}
          {disabled}
          oninput={() => rows = calculateRows(inputValue)}
        />
      </form>
      <!-- 按钮组 -->
      <div class="flex justify-between items-center">
        <!-- 左侧按钮组 -->
        <div class="flex gap-2 items-center">
          <!-- 搜索建议按钮 -->
          <div class="dropdown dropdown-top" class:dropdown-open={showSuggestions}>
            <button
              class="btn btn-ghost btn-neutral btn-circle btn-sm"
              onclick={() => {showSuggestions = !showSuggestions; showAITools = false;}}
              title="建议"
            >
              <Globe class="w-5 h-5" />
            </button>
    
            {#if showSuggestions}
              <div
                class="dropdown-content z-99999 menu p-2 shadow bg-base-100 rounded-box w-64 mt-2"
              >
                {#each suggestions as suggestion}
                  <li>
                    <button
                      class="text-left"
                      onclick={() => handleSuggestionClick(suggestion)}
                    >
                      {suggestion}
                    </button>
                  </li>
                {/each}
              </div>
            {/if}
          </div>

          <!-- AI工具按钮 -->
          <div class="dropdown dropdown-top" class:dropdown-open={showAITools}>
            <button
              class="btn btn-ghost btn-neutral btn-circle btn-sm"
              onclick={() => {showAITools = !showAITools; showSuggestions = false;}}
              title="AI工具"
              disabled={isProcessing}
            >
              <Sparkles class="w-5 h-5" />
            </button>
    
            {#if showAITools}
              <div
                class="dropdown-content z-99999 menu p-2 shadow bg-base-100 rounded-box w-64 mt-2"
              >
                <li>
                  <button
                    class="text-left flex items-center gap-2"
                    onclick={handleQueryMysteriousEvents}
                    disabled={isProcessing}
                  >
                    <Search class="w-4 h-4" /> 查询最近一周的神秘事件
                  </button>
                </li>
                <li>
                  <button
                    class="text-left flex items-center gap-2"
                    onclick={handleExtractEntities}
                    disabled={!inputValue.trim() || isProcessing}
                  >
                    <User class="w-4 h-4" /> 提取文章实体
                  </button>
                </li>
                <li>
                  <button
                    class="text-left flex items-center gap-2"
                    onclick={handleGenerateSummary}
                    disabled={!inputValue.trim() || isProcessing}
                  >
                    <FileText class="w-4 h-4" /> 生成文章摘要
                  </button>
                </li>
                <li>
                  <button
                    class="text-left flex items-center gap-2"
                    onclick={handleGenerateTitle}
                    disabled={!inputValue.trim() || isProcessing}
                  >
                    <Heading class="w-4 h-4" /> 生成文章标题
                  </button>
                </li>
                {#if eventMode && currentEvent}
                  <li>
                    <button
                      class="text-left flex items-center gap-2"
                      onclick={handleAdoptAIAnalysis}
                      disabled={!inputValue.trim() || isProcessing}
                    >
                      <Save class="w-4 h-4" /> 采纳AI分析结果
                    </button>
                  </li>
                {/if}
              </div>
            {/if}
          </div>
        </div>
  
        <!-- 右侧功能按钮组 -->
        <div class="flex gap-2">
          <!-- 生成按钮 -->
          <button
            class="btn btn-sm btn-base-100"
            onclick={handleSubmit}
            disabled={disabled || isProcessing}
          >
            <svg
              class="w-4 h-4"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 16 16"
              fill="currentColor"
            >
              <path
                fill-rule="evenodd"
                d="M5 4a.75.75 0 0 1 .738.616l.252 1.388A1.25 1.25 0 0 0 6.996 7.01l1.388.252a.75.75 0 0 1 0 1.476l-1.388.252A1.25 1.25 0 0 0 5.99 9.996l-.252 1.388a.75.75 0 0 1-1.476 0L4.01 9.996A1.25 1.25 0 0 0 3.004 8.99l-1.388-.252a.75.75 0 0 1 0-1.476l1.388-.252A1.25 1.25 0 0 0 4.01 6.004l.252-1.388A.75.75 0 0 1 5 4ZM12 1a.75.75 0 0 1 .721.544l.195.682c.118.415.443.74.858.858l.682.195a.75.75 0 0 1 0 1.442l-.682.195a1.25 1.25 0 0 0-.858.858l-.195.682a.75.75 0 0 1-1.442 0l-.195-.682a1.25 1.25 0 0 0-.858-.858l-.682-.195a.75.75 0 0 1 0-1.442l.682-.195a1.25 1.25 0 0 0 .858-.858l.195-.682A.75.75 0 0 1 12 1ZM10 11a.75.75 0 0 1 .728.568.968.968 0 0 0 .704.704.75.75 0 0 1 0 1.456.968.968 0 0 0-.704.704.75.75 0 0 1-1.456 0 .968.968 0 0 0-.704-.704.75.75 0 0 1 0-1.456.968.968 0 0 0 .704-.704A.75.75 0 0 1 10 11Z"
                clip-rule="evenodd"
              />
            </svg>
            {isProcessing ? '处理中...' : 'Generate'}
          </button>
        </div>
      </div>
    </div>
  </div>
  
  <p class="text-xs text-base-content/40 text-center mt-1">
    Akasa AI. 回答可能不准确或不完整。
  </p>
</div>

