<script lang="ts">
  import { cn } from "$lib/utils";
  import { Button } from "$lib/components/ui/button";
  import {
    Plus,
    Edit,
    Trash2,
    Lightbulb,
    ChevronDown,
    ChevronUp,
    Check,
    X,
  } from "lucide-svelte";
  import { ScrollArea } from "$lib/components/ui/scroll-area";
  import type { Hypothesis } from "$lib/types/timeline";
  import { createEventDispatcher } from "svelte";
  import { slide } from "svelte/transition";
  import { Input } from "$lib/components/ui/input";
  import { Textarea } from "$lib/components/ui/textarea";
  import { Badge } from "$lib/components/ui/badge";
  import TiltedCard from "$lib/components/ui/tilted-card/tilted-card.svelte";

  // 创建事件分发器
  const dispatch = createEventDispatcher<{
    hypothesisChange: { hypotheses: Hypothesis[] };
    toggleCard: void;
  }>();

  // 组件属性
  let { hypotheses = $bindable([]), className = "" } = $props<{
    hypotheses: Hypothesis[];
    class?: string;
  }>();

  // 导出 class
  export { className as class };

  // 状态变量
  let isAddingHypothesis = $state(false);
  let editingHypothesisId = $state<string | null>(null);
  let newHypothesisTitle = $state("");
  let newHypothesisDescription = $state("");
  let newHypothesisEvidence = $state("");
  let expandedHypothesisId = $state<string | null>(null);

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
    dispatch("hypothesisChange", { hypotheses });
  }

  // 编辑假说
  function startEditHypothesis(hypothesis: Hypothesis) {
    editingHypothesisId = hypothesis.id;
    newHypothesisTitle = hypothesis.title;
    newHypothesisDescription = hypothesis.description;
    newHypothesisEvidence = hypothesis.evidence.join("\n");
  }

  // 保存编辑的假说
  function saveEditHypothesis() {
    if (!newHypothesisTitle.trim()) return;

    hypotheses = hypotheses.map((h: Hypothesis) => {
      if (h.id === editingHypothesisId) {
        return {
          ...h,
          title: newHypothesisTitle.trim(),
          description: newHypothesisDescription.trim(),
          evidence: newHypothesisEvidence.trim()
            ? newHypothesisEvidence
                .split("\n")
                .map((e) => e.trim())
                .filter(Boolean)
            : [],
        };
      }
      return h;
    });

    resetForm();
    dispatch("hypothesisChange", { hypotheses });
  }

  // 删除假说
  function deleteHypothesis(id: string) {
    hypotheses = hypotheses.filter((h: Hypothesis) => h.id !== id);
    dispatch("hypothesisChange", { hypotheses });
  }

  // 重置表单
  function resetForm() {
    isAddingHypothesis = false;
    editingHypothesisId = null;
    newHypothesisTitle = "";
    newHypothesisDescription = "";
    newHypothesisEvidence = "";
  }

  // 切换假说展开/折叠状态
  function toggleHypothesisExpand(id: string) {
    expandedHypothesisId = expandedHypothesisId === id ? null : id;
  }

  // 格式化日期
  function formatDate(date: Date): string {
    return date.toLocaleDateString("zh-CN", {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
    });
  }

  // 获取随机倾斜角度
  function getRandomTilt(id: string): number {
    // 使用ID的哈希值来确定倾斜角度，这样同一个假说总是有相同的倾斜角度
    const hash = id
      .split("")
      .reduce((acc, char) => acc + char.charCodeAt(0), 0);
    // 生成 -8 到 8 之间的随机角度
    return (hash % 17) - 8;
  }

  // 获取随机背景色
  function getRandomBgClass(id: string): string {
    const bgColors = [
      "bg-blue-100/50 dark:bg-blue-900/20",
      "bg-green-100/50 dark:bg-green-900/20",
      "bg-yellow-100/50 dark:bg-yellow-900/20",
      "bg-purple-100/50 dark:bg-purple-900/20",
      "bg-pink-100/50 dark:bg-pink-900/20",
      "bg-indigo-100/50 dark:bg-indigo-900/20",
    ];

    const hash = id
      .split("")
      .reduce((acc, char) => acc + char.charCodeAt(0), 0);
    return bgColors[hash % bgColors.length];
  }
</script>

<div class={cn("w-full py-3", className)}>
  <!-- 头部按钮区 -->
  <div class="flex justify-between items-center mb-4">
    <div class="flex items-center gap-2">
      {#if hypotheses.length > 0}
        <Badge variant="outline">{hypotheses.length} 假说</Badge>
      {/if}
    </div>
    <div class="flex items-center gap-1">
      <Button
        variant="ghost"
        size="sm"
        class="h-7 w-7 p-0"
        onclick={() => (isAddingHypothesis = true)}
      >
        <Plus class="h-4 w-4" />
      </Button>
      <Button
        variant="ghost"
        size="sm"
        class="h-7 w-7 p-0"
        onclick={() => dispatch("toggleCard")}
      >
        <ChevronUp class="h-4 w-4" />
      </Button>
    </div>
  </div>

  <!-- 添加/编辑表单 -->
  {#if isAddingHypothesis || editingHypothesisId}
    <TiltedCard
      tiltAngle={-3}
      bgClass="bg-primary/5 dark:bg-primary/10"
      cardClass="px-6 py-6 relative mx-auto rounded-lg shadow-md bg-card dark:bg-card/90 backdrop-blur-xl"
      class="mb-6"
    >
      <div class="space-y-3">
        <div>
          <label for="hypothesis-title" class="text-xs font-medium mb-1 block"
            >标题</label
          >
          <Input
            id="hypothesis-title"
            bind:value={newHypothesisTitle}
            placeholder="输入假说标题"
          />
        </div>

        <div>
          <label
            for="hypothesis-description"
            class="text-xs font-medium mb-1 block">描述</label
          >
          <Textarea
            id="hypothesis-description"
            bind:value={newHypothesisDescription}
            placeholder="描述这个假说的详细内容"
            rows={2}
          />
        </div>

        <div>
          <label
            for="hypothesis-evidence"
            class="text-xs font-medium mb-1 block">支持证据（每行一条）</label
          >
          <Textarea
            id="hypothesis-evidence"
            bind:value={newHypothesisEvidence}
            placeholder="列出支持这个假说的证据"
            rows={3}
          />
        </div>

        <div class="flex justify-end gap-2 pt-2">
          <Button variant="outline" size="sm" onclick={resetForm}>
            <X class="h-3.5 w-3.5 mr-1" />
            取消
          </Button>
          <Button
            size="sm"
            onclick={editingHypothesisId ? saveEditHypothesis : addHypothesis}
          >
            <Check class="h-3.5 w-3.5 mr-1" />
            {editingHypothesisId ? "保存" : "添加"}
          </Button>
        </div>
      </div>
    </TiltedCard>
  {/if}

  <!-- 假说列表 -->
  {#if hypotheses.length === 0 && !isAddingHypothesis}
    <div class="text-center py-6 text-muted-foreground">
      <Lightbulb class="h-8 w-8 mx-auto mb-2 opacity-50" />
      <p>暂无假说</p>
      <p class="text-xs mt-1">点击右上角的加号添加假说</p>
    </div>
  {:else}
    <div class="space-y-6">
      {#each hypotheses as hypothesis}
        {#if hypothesis.id !== editingHypothesisId}
          <TiltedCard
            tiltAngle={getRandomTilt(hypothesis.id)}
            bgClass={getRandomBgClass(hypothesis.id)}
            cardClass="px-5 py-4 relative mx-auto rounded-lg shadow-md bg-card dark:bg-card/90 backdrop-blur-xl"
          >
            <div class="flex justify-between items-start">
              <button
                type="button"
                class="flex-1 cursor-pointer text-left bg-transparent border-0 p-0"
                onclick={() => toggleHypothesisExpand(hypothesis.id)}
              >
                <div class="flex items-center gap-1">
                  <h4 class="font-medium text-sm">{hypothesis.title}</h4>
                  <Button variant="ghost" size="icon" class="h-5 w-5 p-0 ml-1">
                    {#if expandedHypothesisId === hypothesis.id}
                      <ChevronUp class="h-3 w-3" />
                    {:else}
                      <ChevronDown class="h-3 w-3" />
                    {/if}
                  </Button>
                </div>

                {#if hypothesis.description && expandedHypothesisId !== hypothesis.id}
                  <p class="text-xs mt-1 line-clamp-1 text-muted-foreground">
                    {hypothesis.description}
                  </p>
                {/if}
              </button>

              <div class="flex gap-1 ml-2">
                <Button
                  variant="ghost"
                  size="icon"
                  class="h-6 w-6 bg-white/40 dark:bg-black/20"
                  onclick={() => startEditHypothesis(hypothesis)}
                >
                  <Edit class="h-3 w-3" />
                </Button>
                <Button
                  variant="ghost"
                  size="icon"
                  class="h-6 w-6 bg-white/40 dark:bg-black/20 text-red-600"
                  onclick={() => deleteHypothesis(hypothesis.id)}
                >
                  <Trash2 class="h-3 w-3" />
                </Button>
              </div>
            </div>

            {#if expandedHypothesisId === hypothesis.id}
              <div class="mt-2" in:slide={{ duration: 200 }}>
                {#if hypothesis.description}
                  <p class="text-xs mb-2">{hypothesis.description}</p>
                {/if}

                {#if hypothesis.evidence.length > 0}
                  <div class="mt-2 bg-white/50 dark:bg-white/5 p-2 rounded">
                    <h5 class="text-xs font-medium mb-1">支持证据:</h5>
                    <ul class="text-xs space-y-1 pl-4 list-disc">
                      {#each hypothesis.evidence as evidence}
                        <li>{evidence}</li>
                      {/each}
                    </ul>
                  </div>
                {/if}

                <div class="mt-2 text-xs opacity-70 text-right">
                  创建于: {formatDate(hypothesis.createdAt)}
                </div>
              </div>
            {/if}
          </TiltedCard>
        {/if}
      {/each}
    </div>
  {/if}
</div>
