<script lang="ts">
  import ChatButton from "$lib/components/ai/chat-button.svelte";
  import ChatDialog from "$lib/components/ai/chat-dialog.svelte";
  import { MessageSquare } from "lucide-svelte";
  import { PUBLIC_GEMINI_API_KEY } from "$env/static/public";

  // State
  let dialogOpen = $state(false);
  let apiKey = $state(PUBLIC_GEMINI_API_KEY || "");
  let modelName = $state("gemini-1.5-flash");

  // Sample initial messages for demo
  const sampleMessages = [
    {
      role: "user",
      content: "你好，我想了解一下关于人工智能的最新发展",
      timestamp: new Date()
    },
    {
      role: "model",
      content: "您好！人工智能领域正在快速发展。最近的一些重要进展包括：\n\n1. 大型语言模型（如GPT-4、Claude、Gemini等）的能力不断提升\n2. 多模态AI系统能够同时处理文本、图像、音频等多种输入\n3. AI在医疗、科学研究和创意领域的应用不断扩展\n4. 生成式AI工具变得更加普及和易用\n\n您对哪个方面特别感兴趣？我可以提供更详细的信息。",
      timestamp: new Date()
    }
  ];

  // Methods
  function openDialog() {
    dialogOpen = true;
  }
</script>

<div class="container mx-auto py-8 px-4">
  <h1 class="text-3xl font-bold mb-8 text-center">AI 对话组件演示</h1>

  <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
    <!-- 配置卡片 -->
    <div class="card bg-base-100 shadow-md">
      <div class="card-body">
        <h2 class="card-title">配置</h2>
        <p class="opacity-70">自定义 AI 对话组件的设置</p>

        <div class="form-control w-full">
          <label class="label" for="api-key">
            <span class="label-text">API 密钥</span>
          </label>
          <input
            id="api-key"
            type="password"
            class="input input-bordered w-full"
            bind:value={apiKey}
            placeholder="输入 Google AI API 密钥"
          />
        </div>

        <div class="form-control w-full">
          <label class="label" for="model">
            <span class="label-text">模型</span>
          </label>
          <input
            id="model"
            class="input input-bordered w-full"
            bind:value={modelName}
            placeholder="输入模型名称"
          />
        </div>

        <div class="card-actions justify-end mt-4">
          <button class="btn btn-outline w-full" onclick={openDialog}>
            <MessageSquare class="h-4 w-4 mr-2" />
            打开对话窗口
          </button>
        </div>
      </div>
    </div>

    <!-- 组件展示卡片 -->
    <div class="card bg-base-100 shadow-md">
      <div class="card-body">
        <h2 class="card-title">组件展示</h2>
        <p class="opacity-70">不同样式的 AI 对话按钮</p>

        <div class="space-y-6 mt-4">
          <div>
            <h3 class="font-medium mb-2">默认样式</h3>
            <div class="flex flex-wrap gap-2">
              <ChatButton
                buttonText="开始对话"
                apiKey={apiKey}
                modelName={modelName}
              />
            </div>
          </div>

          <div>
            <h3 class="font-medium mb-2">不同变体</h3>
            <div class="flex flex-wrap gap-2">
              <ChatButton
                buttonVariant="outline"
                buttonText="轮廓样式"
                apiKey={apiKey}
                modelName={modelName}
              />
              <ChatButton
                buttonVariant="secondary"
                buttonText="次要样式"
                apiKey={apiKey}
                modelName={modelName}
              />
              <ChatButton
                buttonVariant="ghost"
                buttonText="幽灵样式"
                apiKey={apiKey}
                modelName={modelName}
              />
            </div>
          </div>

          <div>
            <h3 class="font-medium mb-2">不同尺寸</h3>
            <div class="flex flex-wrap gap-2 items-center">
              <ChatButton
                buttonSize="xs"
                buttonText="超小尺寸"
                apiKey={apiKey}
                modelName={modelName}
              />
              <ChatButton
                buttonSize="sm"
                buttonText="小尺寸"
                apiKey={apiKey}
                modelName={modelName}
              />
              <ChatButton
                buttonText="默认尺寸"
                apiKey={apiKey}
                modelName={modelName}
              />
              <ChatButton
                buttonSize="lg"
                buttonText="大尺寸"
                apiKey={apiKey}
                modelName={modelName}
              />
            </div>
          </div>

          <div>
            <h3 class="font-medium mb-2">带有示例对话</h3>
            <div class="flex flex-wrap gap-2">
              <ChatButton
                buttonText="继续对话"
                buttonVariant="outline"
                apiKey={apiKey}
                modelName={modelName}
                initialMessages={sampleMessages}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- 使用说明 -->
  <div class="card bg-base-100 shadow-md">
    <div class="card-body">
      <h2 class="card-title">使用说明</h2>
      <p class="opacity-70">如何在项目中集成 AI 对话组件</p>

      <div class="space-y-6 mt-4">
        <div>
          <h3 class="text-lg font-medium mb-2">基本用法</h3>
          <div class="mockup-code">
            <pre><code>{`<script>
  import ChatButton from "$lib/components/ai/chat-button.svelte";
  import { PUBLIC_GEMINI_API_KEY } from "$env/static/public";
</script>

<ChatButton
  buttonText="开始对话"
  apiKey={PUBLIC_GEMINI_API_KEY}
  modelName="gemini-1.5-flash"
/>`}</code></pre>
          </div>
        </div>

        <div>
          <h3 class="text-lg font-medium mb-2">直接使用对话框</h3>
          <div class="mockup-code">
            <pre><code>{`<script>
  import ChatDialog from "$lib/components/ai/chat-dialog.svelte";
  import { PUBLIC_GEMINI_API_KEY } from "$env/static/public";

  let dialogOpen = $state(false);
</script>

<button onclick={() => dialogOpen = true}>打开对话</button>

<ChatDialog
  bind:open={dialogOpen}
  apiKey={PUBLIC_GEMINI_API_KEY}
  modelName="gemini-1.5-flash"
  placeholder="有什么可以帮助你的？"
/>`}</code></pre>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- 对话框组件 -->
<ChatDialog
  bind:open={dialogOpen}
  apiKey={apiKey}
  modelName={modelName}
  placeholder="描述你的问题..."
/>
