<script lang="ts">
  import { cn } from "$lib/utils";
  import { Button } from "$lib/components/ui/button";
  import {
    Plus,
    Edit,
    Lightbulb,
    X,
  } from "lucide-svelte";
  import type { Hypothesis } from "$lib/types/timeline";
  import { Input } from "$lib/components/ui/input";
  import { Textarea } from "$lib/components/ui/textarea";

  import { onMount } from "svelte";

  // 添加 CSS 变量
  onMount(() => {
    // 获取 CSS 变量并转换为 RGB 格式
    const convertToRGB = (cssVar: string) => {
      const el = document.createElement('div');
      document.body.appendChild(el);
      el.style.color = `hsl(var(${cssVar}))`;
      const color = window.getComputedStyle(el).color;
      document.body.removeChild(el);

      // 从 "rgb(r, g, b)" 格式中提取 RGB 值
      const match = color.match(/rgb\((\d+),\s*(\d+),\s*(\d+)\)/);
      if (match) {
        return `${match[1]}, ${match[2]}, ${match[3]}`;
      }
      return "0, 0, 0";
    };

    // 设置 RGB 变量
    document.documentElement.style.setProperty('--primary-rgb', convertToRGB('--primary'));
    document.documentElement.style.setProperty('--success-rgb', convertToRGB('--success'));
    document.documentElement.style.setProperty('--destructive-rgb', convertToRGB('--destructive'));
  });

  // 组件属性
  let { hypotheses = $bindable([]), className = "" } = $props<{
    hypotheses: Hypothesis[];
    class?: string;
  }>();

  // 导出 class
  export { className as class };

  // 状态变量
  let editingHypothesisId = $state<string | null>(null);
  let newHypothesisTitle = $state("");
  let newHypothesisDescription = $state("");
  let newHypothesisEvidence = $state("");
  let expandedHypothesisId = $state<string | null>(null);
  let selectedHypothesisId = $state<string | null>(null);
  let isAddingNew = $state(false);

  // 模拟数据 - 在实际应用中应从服务器获取
  let hypothesisVotes = $state<Record<string, { upvotes: number; downvotes: number; voters: Array<{id: string, name: string, avatar: string, vote: 'up' | 'down'}> }>>({});

  // 添加模拟假说数据
  $effect(() => {
    // 如果没有假说，添加一些模拟数据
    if (hypotheses.length === 0) {
      const mockHypotheses: Hypothesis[] = [
        {
          id: crypto.randomUUID(),
          title: "气象变化导致的自然灾害",
          description: "近期异常的气象模式可能导致了这次特大的洪水灾害，包括极端降雨和气温升高。",
          evidence: [
            "过去三个月的降雨量比历史平均高出40%",
            "当地气象站记录到了史上最高的持续降雨天数",
            "卫星图像显示了异常的天气模式"
          ],
          createdAt: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000) // 7天前
        },
        {
          id: crypto.randomUUID(),
          title: "基础设施老化导致的失效",
          description: "当地的水利设施已经运行了50年以上，可能存在结构老化和维护不当的问题。",
          evidence: [
            "大坝最后一次全面检修是在15年前",
            "多个小型水利设施在过去的洪水中已经显示出损坏迹象",
            "当地政府报告显示基础设施维护资金不足"
          ],
          createdAt: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000) // 5天前
        },
        {
          id: crypto.randomUUID(),
          title: "森林砍伐和土地利用变化",
          description: "该地区近年来的大规模森林砍伐和土地开发可能减弱了自然的水流调节能力。",
          evidence: [
            "卫星图像显示该地区森林覆盖率在过去10年中下降了30%",
            "新建的城市开发区位于原本的洪水缓冲区",
            "当地生态学家曾多次警告这种变化的危险"
          ],
          createdAt: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000) // 3天前
        },
        {
          id: crypto.randomUUID(),
          title: "紧急响应系统失效",
          description: "当地的预警和紧急响应系统可能存在重大缺陷，导致没有及时疯狂和有效地应对灾害。",
          evidence: [
            "当地居民报告称没有收到及时的预警",
            "疯狂呼叫在灾害发生后才开始，而非提前",
            "多个紧急避难点的准备不足"
          ],
          createdAt: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000) // 1天前
        }
      ];

      hypotheses = mockHypotheses;
    }
  });

  // 初始化投票数据
  $effect(() => {
    if (hypotheses.length > 0) {
      const newVotes: Record<string, { upvotes: number; downvotes: number; voters: Array<{id: string, name: string, avatar: string, vote: 'up' | 'down'}> }> = {};

      // 为每个假说生成不同的投票模式
      hypotheses.forEach((h: Hypothesis, index: number) => {
        if (!hypothesisVotes[h.id]) {
          // 生成随机投票数，但根据假说索引调整比例
          let upvotes = 0;
          let downvotes = 0;

          switch(index % 4) {
            case 0: // 大多数赞成
              upvotes = 120 + Math.floor(Math.random() * 30);
              downvotes = 20 + Math.floor(Math.random() * 15);
              break;
            case 1: // 差不多平均
              upvotes = 70 + Math.floor(Math.random() * 20);
              downvotes = 60 + Math.floor(Math.random() * 20);
              break;
            case 2: // 大多数反对
              upvotes = 30 + Math.floor(Math.random() * 20);
              downvotes = 90 + Math.floor(Math.random() * 30);
              break;
            case 3: // 压倒性赞成
              upvotes = 180 + Math.floor(Math.random() * 40);
              downvotes = 10 + Math.floor(Math.random() * 10);
              break;
            default:
              upvotes = 100 + Math.floor(Math.random() * 50);
              downvotes = 50 + Math.floor(Math.random() * 30);
          }

          // 生成模拟用户
          const voters = [];
          const totalVoters = Math.min(12, Math.floor((upvotes + downvotes) / 20));

          const userNames = [
            '张三', '李四', '王五', '赵六', '刘七', '陈八',
            '林九', '黄十', '吴大壹', '郑大贰', '孙大叉', '周大肆',
            '吴小凡', '郭小宁', '马小兵', '贾小兵', '宋小宝', '唐小美'
          ];

          for (let i = 0; i < totalVoters; i++) {
            const isUpvote = i < (totalVoters * upvotes / (upvotes + downvotes));
            const randomNameIndex = Math.floor(Math.random() * userNames.length);

            voters.push({
              id: `user-${h.id.substring(0, 4)}-${i}`,
              name: userNames[randomNameIndex],
              avatar: `https://api.dicebear.com/7.x/avataaars/svg?seed=${h.id}-${i}&backgroundColor=${isUpvote ? '4CAF50' : 'F44336'}`,
              vote: isUpvote ? 'up' as const : 'down' as const
            });
          }

          newVotes[h.id] = { upvotes, downvotes, voters };
        } else {
          newVotes[h.id] = hypothesisVotes[h.id];
        }
      });

      hypothesisVotes = newVotes;

      // 默认选中第一个假说
      if (selectedHypothesisId === null && hypotheses.length > 0) {
        selectedHypothesisId = hypotheses[0].id;
      }
    }
  });

  // 添加新假说
  function addHypothesis() {
    if (!newHypothesisTitle.trim()) return;

    const newHypothesis: Hypothesis = {
      id: crypto.randomUUID(),
      title: newHypothesisTitle.trim(),
      description: newHypothesisDescription.trim(),
      evidence: newHypothesisEvidence.trim()
        ? newHypothesisEvidence
            .split("\n")
            .map((e) => e.trim())
            .filter(Boolean)
        : [],
      createdAt: new Date(),
    };

    hypotheses = [...hypotheses, newHypothesis];
    resetForm();
  }

  // 编辑假说
  function startEditHypothesis(hypothesis: Hypothesis) {
    editingHypothesisId = hypothesis.id;
    newHypothesisTitle = hypothesis.title;
    newHypothesisDescription = hypothesis.description;
    newHypothesisEvidence = hypothesis.evidence.join("\n");
  }

  // 重置表单
  function resetForm() {
    editingHypothesisId = null;
    newHypothesisTitle = "";
    newHypothesisDescription = "";
    newHypothesisEvidence = "";
  }
</script>

<div class={cn("w-full py-3 relative", className)}>
  <!-- 假说导航区域 -->
  <div class="flex items-center justify-between mb-4">
    <div class="flex items-center gap-2 overflow-x-auto py-1 no-scrollbar">
      {#if hypotheses.length === 0}
        <div class="text-muted-foreground text-sm">暂无假说</div>
      {:else}
        <div class="relative flex items-center bg-muted/20 rounded-full p-1 backdrop-blur-sm">
          {#each hypotheses as hypothesis, index}
            {@const votes = hypothesisVotes[hypothesis.id] || { upvotes: 0, downvotes: 0 }}
            {@const total = votes.upvotes + votes.downvotes}
            {@const upvotePercentage = total > 0 ? (votes.upvotes / total) * 100 : 75}
            {@const isSelected = selectedHypothesisId === hypothesis.id}

            <button
              class={cn(
                "relative flex-shrink-0 transition-all duration-300 ease-out",
                isSelected ? "scale-100 z-10" : "scale-90 hover:scale-95 z-0"
              )}
              onclick={() => selectedHypothesisId = hypothesis.id}
            >
              <div
                class={cn(
                  "relative w-6 h-6 flex items-center justify-center rounded-full transition-all duration-300",
                  isSelected
                    ? "bg-background shadow-lg"
                    : "bg-background/80"
                )}
              >
                <!-- 光晕效果 -->
                <div
                  class={cn(
                    "absolute inset-0 rounded-full opacity-0 transition-opacity duration-500",
                    isSelected ? "opacity-100" : ""
                  )}
                  style="background: radial-gradient(circle at center, rgba(var(--primary-rgb), 0.15) 0%, transparent 70%);"
                ></div>

                <!-- 环形进度 -->
                <svg class="absolute inset-0 w-full h-full" viewBox="0 0 48 48">
                  <!-- 赞成部分 -->
                  <circle
                    cx="24"
                    cy="24"
                    r="22"
                    fill="none"
                    stroke="url(#gradientSuccess-{index})"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-dasharray="{upvotePercentage * 0.01 * 2 * Math.PI * 22} {2 * Math.PI * 22}"
                    stroke-dashoffset="{2 * Math.PI * 22 * 0.25}"
                    transform="rotate(-90 24 24)"
                    class="transition-all duration-700 ease-out"
                    style="filter: drop-shadow(0 0 3px rgba(var(--success-rgb), 0.5));"
                  />

                  <!-- 反对部分 -->
                  {#if total > 0}
                    <circle
                      cx="24"
                      cy="24"
                      r="22"
                      fill="none"
                      stroke="url(#gradientDestructive-{index})"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-dasharray="{(100 - upvotePercentage) * 0.01 * 2 * Math.PI * 22} {2 * Math.PI * 22}"
                      stroke-dashoffset="{2 * Math.PI * 22 * 0.25}"
                      transform="rotate(-90 24 24)"
                      class="transition-all duration-700 ease-out"
                      style="filter: drop-shadow(0 0 3px rgba(var(--destructive-rgb), 0.5));"
                    />
                  {/if}

                  <!-- 渐变定义 -->
                  <defs>
                    <linearGradient id="gradientSuccess-{index}" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" stop-color="hsl(var(--success))" />
                      <stop offset="100%" stop-color="hsl(var(--success) / 0.7)" />
                    </linearGradient>
                    <linearGradient id="gradientDestructive-{index}" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" stop-color="hsl(var(--destructive))" />
                      <stop offset="100%" stop-color="hsl(var(--destructive) / 0.7)" />
                    </linearGradient>
                  </defs>
                </svg>

                <!-- 数字 -->
                <span
                  class={cn(
                    "text-base font-semibold z-10 transition-all duration-300",
                    isSelected
                      ? "text-primary scale-110"
                      : "text-foreground/80"
                  )}
                >
                  {index + 1}
                </span>

                <!-- 投票比例指示器 -->
                {#if total > 0}
                  <div
                    class="absolute -top-1 -right-1 w-4 h-4 rounded-full bg-background flex items-center justify-center shadow-sm"
                    style="background: conic-gradient(hsl(var(--success)) {upvotePercentage}%, hsl(var(--destructive)) 0%);"
                  >
                    <div class="w-2 h-2 rounded-full bg-background"></div>
                  </div>
                {/if}
              </div>
            </button>
          {/each}
        </div>
      {/if}
    </div>

    <Button
      variant="outline"
      size="sm"
      class="flex-shrink-0 gap-1 text-xs"
      onclick={() => {
        isAddingNew = true;
        selectedHypothesisId = null;
      }}
    >
      <Plus class="h-3 w-3" />
      <span>添加假说</span>
    </Button>
  </div>

  <!-- 假说卡片内容 -->
  <div class="w-full h-[260px] overflow-hidden relative rounded-xl border border-border/50 bg-gradient-to-br from-background to-muted/30 backdrop-blur-sm shadow-lg">
    <!-- 背景装饰元素 -->
    <div class="absolute inset-0 overflow-hidden opacity-10">
      <div class="absolute -right-10 -top-10 w-40 h-40 rounded-full bg-primary/20 blur-3xl"></div>
      <div class="absolute -left-10 -bottom-10 w-40 h-40 rounded-full bg-success/20 blur-3xl"></div>
      <div class="absolute right-1/3 bottom-1/3 w-20 h-20 rounded-full bg-destructive/20 blur-2xl"></div>
    </div>

    {#if isAddingNew}
      <!-- 添加新假说表单 -->
      <div class="p-5 h-full flex flex-col relative z-10">
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center gap-2">
            <div class="w-1 h-6 bg-primary rounded-full"></div>
            <h3 class="text-lg font-medium">添加新假说</h3>
          </div>
          <Button
            variant="ghost"
            size="sm"
            class="h-8 w-8 p-0 rounded-full hover:bg-destructive/10 hover:text-destructive transition-colors"
            onclick={() => {
              isAddingNew = false;
              resetForm();
              if (hypotheses.length > 0) {
                selectedHypothesisId = hypotheses[0].id;
              }
            }}
          >
            <X class="h-4 w-4" />
          </Button>
        </div>

        <div class="space-y-4 flex-1 overflow-y-auto pr-1">
          <div class="group">
            <Input
              placeholder="假说标题"
              bind:value={newHypothesisTitle}
              class="border-muted/50 focus-visible:ring-primary/30 bg-background/50 backdrop-blur-sm transition-all group-focus-within:shadow-[0_0_0_3px_rgba(var(--primary-rgb),0.1)]"
            />
          </div>
          <div class="group">
            <Textarea
              placeholder="假说描述"
              bind:value={newHypothesisDescription}
              class="min-h-[80px] border-muted/50 focus-visible:ring-primary/30 bg-background/50 backdrop-blur-sm transition-all group-focus-within:shadow-[0_0_0_3px_rgba(var(--primary-rgb),0.1)]"
            />
          </div>
          <div class="group">
            <Textarea
              placeholder="支持证据（每行一条）"
              bind:value={newHypothesisEvidence}
              class="min-h-[60px] border-muted/50 focus-visible:ring-primary/30 bg-background/50 backdrop-blur-sm transition-all group-focus-within:shadow-[0_0_0_3px_rgba(var(--primary-rgb),0.1)]"
            />
          </div>
        </div>

        <div class="flex justify-end gap-2 mt-4">
          <Button
            variant="outline"
            class="border-muted/50 bg-background/50 backdrop-blur-sm hover:bg-background/80"
            onclick={() => {
              isAddingNew = false;
              resetForm();
              if (hypotheses.length > 0) {
                selectedHypothesisId = hypotheses[0].id;
              }
            }}
          >
            取消
          </Button>
          <Button
            class="shadow-lg hover:shadow-primary/20 transition-all"
            onclick={() => {
              addHypothesis();
              isAddingNew = false;
              if (hypotheses.length > 0) {
                selectedHypothesisId = hypotheses[hypotheses.length - 1].id;
              }
            }}
            disabled={!newHypothesisTitle.trim()}
          >
            保存
          </Button>
        </div>
      </div>
    {:else if selectedHypothesisId && hypotheses.length > 0}
      <!-- 显示选中的假说 -->
      {@const hypothesis = hypotheses.find((h: Hypothesis) => h.id === selectedHypothesisId)}
      {@const votes = hypothesisVotes[selectedHypothesisId] || { upvotes: 0, downvotes: 0, voters: [] }}
      {@const upvotePercentage = votes.upvotes + votes.downvotes > 0 ? Math.round((votes.upvotes / (votes.upvotes + votes.downvotes)) * 100) : 0}

      {#if hypothesis}
        <div class="p-5 h-full flex flex-col relative z-10">
          <div class="flex items-center justify-between mb-3">
            <div class="flex-1 flex items-center gap-2 overflow-hidden">
              <div class="w-1 h-6 bg-primary rounded-full flex-shrink-0"></div>
              <h3 class="text-lg font-medium line-clamp-1">{hypothesis.title}</h3>
            </div>
            <Button
              variant="ghost"
              size="sm"
              class="h-8 w-8 p-0 rounded-full flex-shrink-0 hover:bg-primary/10 hover:text-primary transition-colors"
              onclick={() => startEditHypothesis(hypothesis)}
            >
              <Edit class="h-4 w-4" />
            </Button>
          </div>

          <div class="text-sm text-muted-foreground mb-4 line-clamp-2 bg-muted/20 p-3 rounded-lg backdrop-blur-sm">
            {hypothesis.description || '暂无描述'}
          </div>

          <!-- 投票统计 -->
          <div class="flex items-stretch gap-3 mb-4 bg-muted/10 rounded-lg p-2 backdrop-blur-sm">
            <!-- 进度条 -->
            <div class="flex-1 h-10 relative bg-muted/30 rounded-md overflow-hidden">
              <div
                class="absolute inset-y-0 left-0 bg-gradient-to-r from-success/80 to-success/60 transition-all duration-500 ease-out"
                style="width: {upvotePercentage}%"
              ></div>
              <div class="absolute inset-0 flex items-center justify-between px-3">
                <div class="flex items-center gap-1.5 z-10">
                  <div class="w-2 h-2 rounded-full bg-success"></div>
                  <span class="text-sm font-medium">{votes.upvotes}</span>
                </div>
                <div class="text-xs font-semibold z-10 bg-background/50 px-2 py-0.5 rounded-full">
                  {upvotePercentage}%
                </div>
                <div class="flex items-center gap-1.5 z-10">
                  <span class="text-sm font-medium">{votes.downvotes}</span>
                  <div class="w-2 h-2 rounded-full bg-destructive"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- 投票用户头像 -->
          <div class="mt-auto">
            <h4 class="text-xs font-medium text-muted-foreground mb-2 flex items-center gap-1">
              <div class="w-1 h-3 bg-primary/50 rounded-full"></div>
              投票用户
            </h4>
            <div class="flex flex-wrap gap-1.5">
              {#if votes.voters.length === 0}
                <div class="text-xs text-muted-foreground bg-muted/20 px-2 py-1 rounded-md">暂无投票</div>
              {:else}
                {#each votes.voters as voter}
                  <div
                    class={cn(
                      "relative w-7 h-7 rounded-full overflow-hidden transition-transform hover:scale-110 hover:z-10",
                      voter.vote === 'up'
                        ? "ring-2 ring-success/30 ring-offset-1 ring-offset-background shadow-[0_0_5px_rgba(var(--success-rgb),0.3)]"
                        : "ring-2 ring-destructive/30 ring-offset-1 ring-offset-background shadow-[0_0_5px_rgba(var(--destructive-rgb),0.3)]"
                    )}
                  >
                    <img
                      src={voter.avatar}
                      alt={voter.name}
                      class="w-full h-full object-cover"
                    />
                  </div>
                {/each}
              {/if}
            </div>
          </div>
        </div>
      {/if}
    {:else}
      <!-- 空状态 -->
      <div class="flex flex-col items-center justify-center h-full p-4 text-center relative z-10">
        <div class="absolute inset-0 bg-gradient-to-b from-primary/5 to-background/0 opacity-50"></div>
        <div class="relative z-10">
          <div class="w-16 h-16 rounded-full bg-muted/30 flex items-center justify-center mb-4 mx-auto backdrop-blur-sm">
            <Lightbulb class="h-8 w-8 text-primary/70" />
          </div>
          <h3 class="text-lg font-medium mb-2">添加事件假说</h3>
          <p class="text-sm text-muted-foreground mb-5 max-w-xs mx-auto">提出对事件原因或过程的猜想和假说</p>
          <Button
            class="shadow-lg hover:shadow-primary/20 transition-all"
            onclick={() => {
              isAddingNew = true;
            }}
          >
            <Plus class="h-4 w-4 mr-2" />
            添加假说
          </Button>
        </div>
      </div>
    {/if}
  </div>
</div>
