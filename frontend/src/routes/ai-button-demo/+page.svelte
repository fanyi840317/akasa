<script lang="ts">
  import { onMount } from "svelte";
  import { EdgelessAIToolButton } from "$lib/components/editor/toolbar/ai/ai-button";
  import AIModal from "$lib/components/editor/toolbar/ai/ai-modal.svelte";
  import AIFeatureHandler from "$lib/components/editor/toolbar/ai/ai-feature-handler.svelte";

  // 注册自定义元素
  if (!customElements.get("edgeless-ai-tool-button")) {
    customElements.define("edgeless-ai-tool-button", EdgelessAIToolButton);
  }

  // 状态管理
  let aiButtonRef: HTMLDivElement;
  let showAIModal = $state(false);
  let aiModalPosition = $state({ x: 0, y: 0 });
  let activeAIFeature = $state("");

  // AI按钮处理函数
  function handleAIClick() {
    const rect = aiButtonRef?.getBoundingClientRect();
    if (rect) {
      aiModalPosition = {
        x: rect.left + rect.width / 2,
        y: rect.top
      };
    }
    showAIModal = true;
  }

  function handleAIFeatureSelect(event: CustomEvent) {
    activeAIFeature = event.detail.featureId;
    showAIModal = false;
  }

  function handleAIModalClose() {
    showAIModal = false;
  }

  function handleAIFeatureClose() {
    activeAIFeature = "";
  }
</script>

<div class="min-h-screen bg-gray-100 p-8">
  <div class="max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold text-center mb-8">AI 按钮组件演示</h1>
    
    <!-- 演示区域 -->
    <div class="bg-white rounded-lg shadow-lg p-8 mb-8">
      <h2 class="text-xl font-semibold mb-4">AI 工具按钮</h2>
      <p class="text-gray-600 mb-6">
        点击下面的AI按钮来体验功能选择模态框和各种AI功能。
      </p>
      
      <!-- AI按钮容器 -->
      <div class="flex justify-center items-center py-12 bg-gray-50 rounded-lg">
        <edgeless-ai-tool-button
          bind:this={aiButtonRef}
          onclick={handleAIClick}
        ></edgeless-ai-tool-button>
      </div>
    </div>

    <!-- 功能说明 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div class="bg-white rounded-lg shadow p-6">
        <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
          <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
          </svg>
        </div>
        <h3 class="text-lg font-semibold mb-2">AI 对话</h3>
        <p class="text-gray-600 text-sm">与AI助手进行智能对话，获取帮助和建议。</p>
      </div>

      <div class="bg-white rounded-lg shadow p-6">
        <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
          <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
          </svg>
        </div>
        <h3 class="text-lg font-semibold mb-2">图像生成</h3>
        <p class="text-gray-600 text-sm">使用AI生成创意图像和视觉内容。</p>
      </div>

      <div class="bg-white rounded-lg shadow p-6">
        <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
          <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
        </div>
        <h3 class="text-lg font-semibold mb-2">文本生成</h3>
        <p class="text-gray-600 text-sm">智能文本创作，包括文章、邮件等内容。</p>
      </div>

      <div class="bg-white rounded-lg shadow p-6">
        <div class="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center mb-4">
          <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
          </svg>
        </div>
        <h3 class="text-lg font-semibold mb-2">创意灵感</h3>
        <p class="text-gray-600 text-sm">获取创意想法和项目灵感。</p>
      </div>

      <div class="bg-white rounded-lg shadow p-6">
        <div class="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center mb-4">
          <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
          </svg>
        </div>
        <h3 class="text-lg font-semibold mb-2">内容优化</h3>
        <p class="text-gray-600 text-sm">优化和改进现有的文本内容。</p>
      </div>

      <div class="bg-white rounded-lg shadow p-6">
        <div class="w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center mb-4">
          <svg class="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
          </svg>
        </div>
        <h3 class="text-lg font-semibold mb-2">智能分析</h3>
        <p class="text-gray-600 text-sm">分析和总结各种类型的内容。</p>
      </div>
    </div>

    <!-- 使用说明 -->
    <div class="bg-white rounded-lg shadow-lg p-8 mt-8">
      <h2 class="text-xl font-semibold mb-4">使用说明</h2>
      <div class="space-y-4 text-gray-600">
        <p>
          <strong>1. 点击AI按钮：</strong> 点击上方的彩色AI按钮，会弹出功能选择模态框。
        </p>
        <p>
          <strong>2. 选择功能：</strong> 在模态框中选择您需要的AI功能，如对话、图像生成等。
        </p>
        <p>
          <strong>3. 开始使用：</strong> 选择功能后会打开相应的AI对话界面，您可以开始与AI交互。
        </p>
        <p>
          <strong>4. 关闭对话：</strong> 完成后可以关闭对话框，返回到编辑器界面。
        </p>
      </div>
    </div>
  </div>
</div>

<!-- AI模态框 -->
<AIModal 
  bind:open={showAIModal}
  position={aiModalPosition}
  on:feature-select={handleAIFeatureSelect}
  on:close={handleAIModalClose}
/>

<!-- AI功能处理器 -->
<AIFeatureHandler 
  bind:activeFeature={activeAIFeature}
  position={aiModalPosition}
  on:close={handleAIFeatureClose}
/>
