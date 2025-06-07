<script lang="ts">
  import CenteredChatInput from "$lib/components/ai/centered-chat-input.svelte";
  import { PUBLIC_GEMINI_API_KEY } from "$env/static/public";
  import { mode } from "mode-watcher";

  // State
  let apiKey = $state(PUBLIC_GEMINI_API_KEY || "");
  let showToolbar = $state(true);
  let aspectRatio = $state("2:3");
  let inputMode = $state("4v");
  let activeTab = $state("demo");

  // Toggle dark mode
  function toggleDarkMode() {
    if ($mode === "dark") {
      mode.set("light");
    } else {
      mode.set("dark");
    }
  }
</script>

<div class="container mx-auto py-8 px-4">
  <h1 class="text-3xl font-bold mb-2 text-center">中央对话输入组件</h1>
  <p class="text-center opacity-60 mb-8">
    类似于 Google AI 的中央对话输入框
  </p>

  <!-- Dark Mode Toggle -->
  <div class="flex justify-end mb-4">
    <button class="btn btn-outline btn-sm" onclick={toggleDarkMode}>
      {$mode === "dark" ? "切换到亮色模式" : "切换到暗色模式"}
    </button>
  </div>

  <!-- Demo Tabs -->
  <div class="mb-8">
    <div class="tabs tabs-boxed justify-center max-w-md mx-auto">
      <button
        class="tab {activeTab === 'demo' ? 'tab-active' : ''}"
        onclick={() => activeTab = 'demo'}
        onkeydown={(e) => e.key === 'Enter' && (activeTab = 'demo')}
        role="tab"
        aria-selected={activeTab === 'demo'}
      >
        演示
      </button>
      <button
        class="tab {activeTab === 'config' ? 'tab-active' : ''}"
        onclick={() => activeTab = 'config'}
        onkeydown={(e) => e.key === 'Enter' && (activeTab = 'config')}
        role="tab"
        aria-selected={activeTab === 'config'}
      >
        配置
      </button>
    </div>

    {#if activeTab === 'demo'}
      <!-- Main Demo Area -->
      <div class="flex items-center justify-center min-h-[400px] bg-base-200 rounded-lg p-4 mt-4">
        <CenteredChatInput
          apiKey={apiKey}
          {showToolbar}
          aspectRatio={aspectRatio}
          mode={inputMode}
          placeholder="描述你的图片..."
        />
      </div>
    {:else}
      <!-- Configuration Card -->
      <div class="card bg-base-100 shadow-md max-w-md mx-auto mt-4">
        <div class="card-body">
          <h2 class="card-title">组件配置</h2>
          <p class="opacity-70">自定义中央对话输入组件的外观和行为</p>

          <div class="form-control w-full">
            <label class="label" for="api-key">
              <span class="label-text">Google AI API 密钥</span>
            </label>
            <input
              id="api-key"
              type="password"
              class="input input-bordered w-full"
              bind:value={apiKey}
              placeholder="输入 API 密钥"
            />
          </div>

          <div class="form-control">
            <label class="label cursor-pointer justify-start gap-2">
              <input
                type="checkbox"
                class="checkbox"
                bind:checked={showToolbar}
              />
              <span class="label-text">显示工具栏</span>
            </label>
          </div>

          <fieldset class="form-control">
            <legend class="label-text mb-2">长宽比</legend>
            <div class="btn-group">
              <button
                class="btn {aspectRatio === '2:3' ? 'btn-active' : ''}"
                onclick={() => aspectRatio = "2:3"}
              >
                2:3
              </button>
              <button
                class="btn {aspectRatio === '1:1' ? 'btn-active' : ''}"
                onclick={() => aspectRatio = "1:1"}
              >
                1:1
              </button>
              <button
                class="btn {aspectRatio === '3:2' ? 'btn-active' : ''}"
                onclick={() => aspectRatio = "3:2"}
              >
                3:2
              </button>
            </div>
          </fieldset>

          <fieldset class="form-control">
            <legend class="label-text mb-2">模式</legend>
            <div class="btn-group">
              <button
                class="btn {inputMode === '4v' ? 'btn-active' : ''}"
                onclick={() => inputMode = "4v"}
              >
                4v
              </button>
              <button
                class="btn {inputMode === '图像' ? 'btn-active' : ''}"
                onclick={() => inputMode = "图像"}
              >
                图像
              </button>
            </div>
          </fieldset>
        </div>
      </div>
    {/if}
  </div>

  <!-- Usage Instructions -->
  <div class="card bg-base-100 shadow-md">
    <div class="card-body">
      <h2 class="card-title">使用说明</h2>
      <p class="opacity-70">如何在项目中集成中央对话输入组件</p>

      <div class="mockup-code mt-4">
        <pre><code>{`<script>
  import CenteredChatInput from "$lib/components/ai/centered-chat-input.svelte";
  import { PUBLIC_GEMINI_API_KEY } from "$env/static/public";
</script>

<div class="flex items-center justify-center min-h-[400px]">
  <CenteredChatInput
    apiKey={PUBLIC_GEMINI_API_KEY}
    showToolbar={true}
    aspectRatio="2:3"
    mode="4v"
    placeholder="描述你的图片..."
  />
</div>`}</code></pre>
      </div>

      <div class="mt-4">
        <p class="text-sm opacity-70">
          组件会自动处理对话框的打开和关闭，并使用 Google AI 进行对话。
        </p>
      </div>
    </div>
  </div>
</div>
