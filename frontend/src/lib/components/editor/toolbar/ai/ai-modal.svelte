<script lang="ts">
  import { MessageSquare, Image, FileText, Lightbulb, Zap, Brain, Sparkles, X } from "lucide-svelte";

  let {
    open = $bindable(false),
    position = { x: 0, y: 0 },
    onfeatureselect,
    onclose
  } = $props<{
    open?: boolean;
    position?: { x: number; y: number };
    onfeatureselect?: (event: { featureId: string }) => void;
    onclose?: () => void;
  }>();

  // AI功能卡片数据
  const aiFeatures = [
    {
      id: "chat",
      title: "AI 对话",
      description: "与AI助手进行智能对话",
      icon: MessageSquare,
      color: "from-blue-500 to-blue-600",
      action: () => handleFeatureClick("chat")
    },
    {
      id: "image-gen",
      title: "图像生成",
      description: "AI生成创意图像",
      icon: Image,
      color: "from-purple-500 to-purple-600",
      action: () => handleFeatureClick("image-gen")
    },
    {
      id: "text-gen",
      title: "文本生成",
      description: "智能文本创作助手",
      icon: FileText,
      color: "from-green-500 to-green-600",
      action: () => handleFeatureClick("text-gen")
    },
    {
      id: "ideas",
      title: "创意灵感",
      description: "获取创意想法和建议",
      icon: Lightbulb,
      color: "from-yellow-500 to-yellow-600",
      action: () => handleFeatureClick("ideas")
    },
    {
      id: "optimize",
      title: "内容优化",
      description: "优化和改进现有内容",
      icon: Zap,
      color: "from-red-500 to-red-600",
      action: () => handleFeatureClick("optimize")
    },
    {
      id: "analyze",
      title: "智能分析",
      description: "分析和总结内容",
      icon: Brain,
      color: "from-indigo-500 to-indigo-600",
      action: () => handleFeatureClick("analyze")
    }
  ];

  function handleFeatureClick(featureId: string) {
    onfeatureselect?.({ featureId });
    open = false;
  }

  function closeModal() {
    open = false;
    onclose?.();
  }

  // 计算模态框位置 - 使用 $derived 替代 $:
  const modalStyle = $derived(`
    position: fixed;
    left: ${Math.max(10, Math.min(position.x - 200, typeof window !== 'undefined' ? window.innerWidth - 420 : 400))}px;
    top: ${Math.max(10, Math.min(position.y - 150, typeof window !== 'undefined' ? window.innerHeight - 320 : 300))}px;
    z-index: 9999;
  `);
</script>

{#if open}
  <!-- 背景遮罩 -->
  <div
    class="fixed inset-0 bg-black bg-opacity-50 z-[9998]"
    onclick={closeModal}
    role="button"
    tabindex="0"
    onkeydown={(e) => e.key === 'Enter' && closeModal()}
  ></div>

  <!-- AI功能模态框 -->
  <div
    class="bg-white rounded-xl shadow-2xl border border-gray-200 w-[400px]"

    role="dialog"
    aria-modal="true"
    aria-labelledby="ai-modal-title"
  >
    <!-- 模态框头部 -->
    <div class="flex items-center justify-between p-4 border-b border-gray-200">
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full flex items-center justify-center">
          <Sparkles class="w-4 h-4 text-white" />
        </div>
        <h2 id="ai-modal-title" class="text-lg font-semibold text-gray-800">AI 助手</h2>
      </div>
      <button
        class="p-1 hover:bg-gray-100 rounded-full transition-colors"
        onclick={closeModal}
        aria-label="关闭"
      >
        <X class="w-5 h-5 text-gray-500" />
      </button>
    </div>

    <!-- 功能卡片网格 -->
    <div class="p-4">
      <div class="grid grid-cols-2 gap-3">
        {#each aiFeatures as feature}
          {@const IconComponent = feature.icon}
          <button
            class="group relative p-4 rounded-lg border border-gray-200 hover:border-gray-300
                   hover:shadow-md transition-all duration-200 text-left
                   focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            onclick={feature.action}
          >
            <!-- 渐变背景 -->
            <div class="absolute inset-0 bg-gradient-to-r {feature.color} opacity-0
                        group-hover:opacity-10 rounded-lg transition-opacity duration-200"></div>

            <!-- 图标 -->
            <div class="relative mb-2">
              <div class="w-8 h-8 bg-gradient-to-r {feature.color} rounded-lg
                          flex items-center justify-center group-hover:scale-110
                          transition-transform duration-200">
                <IconComponent class="w-4 h-4 text-white" />
              </div>
            </div>

            <!-- 标题和描述 -->
            <div class="relative">
              <h3 class="font-medium text-gray-800 mb-1 group-hover:text-gray-900">
                {feature.title}
              </h3>
              <p class="text-xs text-gray-600 group-hover:text-gray-700">
                {feature.description}
              </p>
            </div>

            <!-- 悬停效果指示器 -->
            <div class="absolute top-2 right-2 w-2 h-2 bg-gradient-to-r {feature.color}
                        rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-200"></div>
          </button>
        {/each}
      </div>

      <!-- 底部提示 -->
      <div class="mt-4 p-3 bg-gray-50 rounded-lg">
        <p class="text-xs text-gray-600 text-center">
          选择一个AI功能开始使用智能助手
        </p>
      </div>
    </div>
  </div>
{/if}

<style>
  /* 自定义滚动条样式 */
  :global(.ai-modal-content::-webkit-scrollbar) {
    width: 4px;
  }

  :global(.ai-modal-content::-webkit-scrollbar-track) {
    background: #f1f1f1;
    border-radius: 2px;
  }

  :global(.ai-modal-content::-webkit-scrollbar-thumb) {
    background: #c1c1c1;
    border-radius: 2px;
  }

  :global(.ai-modal-content::-webkit-scrollbar-thumb:hover) {
    background: #a8a8a8;
  }
</style>
