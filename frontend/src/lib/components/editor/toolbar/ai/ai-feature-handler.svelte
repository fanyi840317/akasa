<script lang="ts">
  import ChatDialog from "../../../ai/chat-dialog.svelte";
  import { PUBLIC_GEMINI_API_KEY } from "$env/static/public";

  let {
    activeFeature = $bindable(""),
    onclose
  } = $props<{
    activeFeature?: string;
    onclose?: () => void;
  }>();

  // 状态管理
  let chatDialogOpen = $state(false);
  let imageGenDialogOpen = $state(false);
  let textGenDialogOpen = $state(false);
  let ideasDialogOpen = $state(false);
  let optimizeDialogOpen = $state(false);
  let analyzeDialogOpen = $state(false);

  // 监听activeFeature变化 - 使用 $effect 替代 $:
  $effect(() => {
    if (activeFeature) {
      handleFeatureActivation(activeFeature);
    }
  });

  function handleFeatureActivation(featureId: string) {
    // 关闭所有对话框
    closeAllDialogs();

    // 根据功能ID打开相应的对话框
    switch (featureId) {
      case "chat":
        chatDialogOpen = true;
        break;
      case "image-gen":
        imageGenDialogOpen = true;
        break;
      case "text-gen":
        textGenDialogOpen = true;
        break;
      case "ideas":
        ideasDialogOpen = true;
        break;
      case "optimize":
        optimizeDialogOpen = true;
        break;
      case "analyze":
        analyzeDialogOpen = true;
        break;
    }
  }

  function closeAllDialogs() {
    chatDialogOpen = false;
    imageGenDialogOpen = false;
    textGenDialogOpen = false;
    ideasDialogOpen = false;
    optimizeDialogOpen = false;
    analyzeDialogOpen = false;
  }

  function handleDialogClose() {
    activeFeature = "";
    closeAllDialogs();
    onclose?.();
  }

  // 预设的对话消息
  const imageGenMessages = [
    {
      role: "user" as const,
      content: "我想生成一张图片，请帮我描述图片内容",
      timestamp: new Date()
    },
    {
      role: "model" as const,
      content: "我很乐意帮您生成图片！请告诉我您想要什么样的图片，包括：\n\n1. 主题内容（人物、风景、物品等）\n2. 艺术风格（写实、卡通、抽象等）\n3. 色彩偏好\n4. 构图要求\n\n例如：\"一只可爱的橙色小猫坐在窗台上，背景是夕阳西下的城市天际线，温暖的色调，写实风格\"",
      timestamp: new Date()
    }
  ];

  const textGenMessages = [
    {
      role: "user" as const,
      content: "我需要帮助写一些文本内容",
      timestamp: new Date()
    },
    {
      role: "model" as const,
      content: "我很高兴帮您创作文本内容！我可以协助您：\n\n📝 **文章写作** - 博客、新闻、教程\n📧 **邮件起草** - 商务邮件、感谢信\n📱 **社交媒体** - 朋友圈、微博文案\n📋 **工作文档** - 报告、提案、总结\n🎨 **创意写作** - 故事、诗歌、剧本\n\n请告诉我您需要什么类型的文本，以及具体要求！",
      timestamp: new Date()
    }
  ];

  const ideasMessages = [
    {
      role: "user" as const,
      content: "我需要一些创意灵感",
      timestamp: new Date()
    },
    {
      role: "model" as const,
      content: "💡 **创意灵感助手** 为您服务！我可以帮您：\n\n🎯 **项目创意** - 新产品、活动策划\n🎨 **设计灵感** - 视觉设计、UI/UX\n📝 **内容创意** - 文章主题、视频脚本\n🚀 **商业想法** - 创业点子、营销策略\n🎪 **活动策划** - 聚会、会议、庆典\n🎮 **娱乐创意** - 游戏、互动体验\n\n请告诉我您在哪个领域需要创意灵感？",
      timestamp: new Date()
    }
  ];

  const optimizeMessages = [
    {
      role: "user" as const,
      content: "我想优化一些内容",
      timestamp: new Date()
    },
    {
      role: "model" as const,
      content: "🔧 **内容优化专家** 为您服务！我可以帮您优化：\n\n✍️ **文本优化** - 语法、表达、结构\n🎯 **SEO优化** - 关键词、标题、描述\n📧 **邮件优化** - 主题行、正文、CTA\n📱 **社交媒体** - 提高互动率和传播效果\n🎨 **设计建议** - 布局、色彩、字体\n⚡ **性能优化** - 加载速度、用户体验\n\n请分享您想要优化的内容，我会提供具体的改进建议！",
      timestamp: new Date()
    }
  ];

  const analyzeMessages = [
    {
      role: "user" as const,
      content: "我需要分析一些内容",
      timestamp: new Date()
    },
    {
      role: "model" as const,
      content: "🧠 **智能分析助手** 为您服务！我可以帮您分析：\n\n📊 **数据分析** - 趋势、模式、洞察\n📝 **文本分析** - 情感、主题、关键词\n🎯 **竞品分析** - 优劣势、差异化\n👥 **用户分析** - 行为、需求、偏好\n📈 **市场分析** - 机会、威胁、策略\n🔍 **内容审核** - 质量、合规性、改进点\n\n请提供您需要分析的内容或数据，我会为您提供详细的分析报告！",
      timestamp: new Date()
    }
  ];
</script>

<!-- AI对话 -->
<ChatDialog
  bind:open={chatDialogOpen}
  apiKey={PUBLIC_GEMINI_API_KEY}
  modelName="gemini-1.5-flash"
  placeholder="与AI助手对话..."
  onclose={handleDialogClose}
/>

<!-- 图像生成 -->
<ChatDialog
  bind:open={imageGenDialogOpen}
  apiKey={PUBLIC_GEMINI_API_KEY}
  modelName="gemini-1.5-flash"
  placeholder="描述您想要生成的图片..."
  initialMessages={imageGenMessages}
  onclose={handleDialogClose}
/>

<!-- 文本生成 -->
<ChatDialog
  bind:open={textGenDialogOpen}
  apiKey={PUBLIC_GEMINI_API_KEY}
  modelName="gemini-1.5-flash"
  placeholder="告诉我您需要什么类型的文本..."
  initialMessages={textGenMessages}
  onclose={handleDialogClose}
/>

<!-- 创意灵感 -->
<ChatDialog
  bind:open={ideasDialogOpen}
  apiKey={PUBLIC_GEMINI_API_KEY}
  modelName="gemini-1.5-flash"
  placeholder="告诉我您需要什么领域的创意..."
  initialMessages={ideasMessages}
  onclose={handleDialogClose}
/>

<!-- 内容优化 -->
<ChatDialog
  bind:open={optimizeDialogOpen}
  apiKey={PUBLIC_GEMINI_API_KEY}
  modelName="gemini-1.5-flash"
  placeholder="分享您想要优化的内容..."
  initialMessages={optimizeMessages}
  onclose={handleDialogClose}
/>

<!-- 智能分析 -->
<ChatDialog
  bind:open={analyzeDialogOpen}
  apiKey={PUBLIC_GEMINI_API_KEY}
  modelName="gemini-1.5-flash"
  placeholder="提供您需要分析的内容..."
  initialMessages={analyzeMessages}
  onclose={handleDialogClose}
/>
