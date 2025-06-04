<script lang="ts">
  import { cn } from "$lib/utils";
  import { Globe } from "lucide-svelte";

  let showSuggestions = false;
  let rows = $state(2); // 初始行数
  let maxRows = 10; // 最大行数

  // 添加属性
  let {
    disabled = false,
    placeholder = "Ask anything",
    inputValue = $bindable(""),
    class:className,
    onSubmit,
  } = $props<{
    class?: string;
    disabled?: boolean;
    placeholder?: string;
    inputValue?: string;
    onSubmit?: (text: string) => void;
  }>();

  const suggestions = [
    "What is the weather today?",
    "Tell me a joke.",
    "How do I code in JavaScript?",
  ];

  // 根据内容计算行数
  function calculateRows(text: string): number {
    if (!text) return 2; // 默认至少2行
    
    // 计算换行符数量
    const newLines = (text.match(/\n/g) || []).length;
    
    // 估算每行平均字符数（根据实际情况调整）
    const avgCharsPerLine = 50;
    const textLines = Math.ceil(text.length / avgCharsPerLine);
    
    // 取换行符数量和估算行数的较大值，并确保在2-6行之间
    return Math.max(2, Math.min(maxRows, Math.max(newLines + 1, textLines)));
  }

  // 监听输入值变化，更新行数
  $effect(() => {
    rows = calculateRows(inputValue);
  });

  function handleSubmit() {
    if (inputValue.trim()) {
      onSubmit?.(inputValue.trim());
    }
  }

  function handleSuggestionClick(suggestion: string) {
    inputValue = suggestion;
    showSuggestions = false;
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
        <!-- 搜索建议按钮 -->
        <div class="dropdown dropdown-top" class:dropdown-open={showSuggestions}>
          <button
            class="btn btn-ghost btn-neutral btn-circle btn-sm"
            onclick={() => {showSuggestions = !showSuggestions ;}}
          >
            <Globe class="w-5 h-5" />
          </button>
  
          {#if showSuggestions}
            <div
              class="dropdown-content z-99999 menu p-2 shadow bg-base-100 rounded-box w-52 mt-2"
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
  
        <!-- 功能按钮组 -->
        <div class="flex gap-2">
          <!-- 语音输入 -->
  
          <!-- 生成按钮 -->
          <button
            class="btn btn-sm btn-base-100"
            onclick={handleSubmit}
            {disabled}
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
            Generate
          </button>
        </div>
      </div>
    </div>
  </div>
  
  <p class="text-xs text-gray-500 text-center mt-1">
    Akasa AI. 回答可能不准确或不完整。
  </p>
</div>


<style>
  /* 渐变边框效果 */
  .gradient-border {
    position: relative;
    background: linear-gradient(45deg, #0084ff, #00d4ff);
  }

  .gradient-border::before {
    content: "";
    position: absolute;
    inset: -2px;
    padding: 2px;
    background: conic-gradient(from 0deg, #0084ff, #00d4ff, #0084ff);
    border-radius: inherit;
    mask:
      linear-gradient(#fff 0 0) content-box,
      linear-gradient(#fff 0 0);
    mask-composite: xor;
    animation: rotate 3s linear infinite;
  }

  @keyframes rotate {
    to {
      transform: rotate(360deg);
    }
  }

  /* 语音按钮动画 */
  .voice-btn:hover .bar {
    animation: wave 0.6s infinite ease-in-out alternate;
  }

  .bar-1 {
    animation-delay: 0s;
  }
  .bar-2 {
    animation-delay: 0.1s;
  }
  .bar-3 {
    animation-delay: 0.2s;
  }
  .bar-4 {
    animation-delay: 0.3s;
  }

  @keyframes wave {
    0%,
    100% {
      transform: scaleY(1);
    }
    50% {
      transform: scaleY(1.5);
    }
  }
</style>
