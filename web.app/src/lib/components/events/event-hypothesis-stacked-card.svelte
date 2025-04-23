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
    Info,
  } from "lucide-svelte";
  import { ScrollArea } from "$lib/components/ui/scroll-area";
  import type { Hypothesis } from "$lib/types/timeline";
  import { createEventDispatcher } from "svelte";
  import { slide, fade } from "svelte/transition";
  import { Input } from "$lib/components/ui/input";
  import { Textarea } from "$lib/components/ui/textarea";
  import { Badge } from "$lib/components/ui/badge";
  import {
    Popover,
    PopoverContent,
    PopoverTrigger,
  } from "$lib/components/ui/popover";
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
  let showDetails = $state(false);

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
  function getRandomTilt(id: string, index: number): number {
    // 使用ID的哈希值来确定倾斜角度，这样同一个假说总是有相同的倾斜角度
    const hash = id
      .split("")
      .reduce((acc, char) => acc + char.charCodeAt(0), 0);
    // 生成 -5 到 5 之间的随机角度
    return ((hash % 11) - 5) * 0.8;
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

  // 获取堆叠卡片的样式
  function getStackedCardStyle(index: number, total: number): string {
    const maxOffset = 10; // 最大偏移量（像素）
    const maxRotate = 3; // 最大旋转角度
    
    // 计算偏移量和旋转角度
    const offset = (index / (total - 1)) * maxOffset;
    const rotate = ((index / (total - 1)) * 2 - 1) * maxRotate;
    
    return `transform: translateY(${offset}px) rotate(${rotate}deg); z-index: ${100 - index};`;
  }
</script>

<div class={cn("w-full py-3", className)}>
  <!-- 头部按钮区 -->
  <div class="flex justify-between items-center mb-4">
    <div class="flex items-center gap-2">
      {#if hypotheses.length > 0}
        <Badge variant="outline" class="cursor-pointer" onclick={() => showDetails = !showDetails}>
          {hypotheses.length} 假说
          {#if !showDetails}
            <ChevronDown class="h-3 w-3 ml-1" />
          {:else}
            <ChevronUp class="h-3 w-3 ml-1" />
          {/if}
        </Badge>
      {/if}
    </div>
    <div class="flex items-center gap-1">
      <Popover>
        <PopoverTrigger>
          <Button
            variant="ghost"
            size="sm"
            class="h-7 w-7 p-0"
          >
            <Plus class="h-4 w-4" />
          </Button>
        </PopoverTrigger>
        <PopoverContent class="w-80 p-4">
          <div class="space-y-3">
            <h4 class="text-sm font-medium flex items-center gap-2">
              <Lightbulb class="h-4 w-4 text-yellow-500" />
              添加新假说
            </h4>
            <div>
              <label for="hypothesis-title" class="text-xs font-medium mb-1 block">标题</label>
              <Input
                id="hypothesis-title"
                bind:value={newHypothesisTitle}
                placeholder="输入假说标题"
              />
            </div>
            
            <div>
              <label for="hypothesis-description" class="text-xs font-medium mb-1 block">描述</label>
              <Textarea
                id="hypothesis-description"
                bind:value={newHypothesisDescription}
                placeholder="描述这个假说的详细内容"
                rows={2}
              />
            </div>
            
            <div>
              <label for="hypothesis-evidence" class="text-xs font-medium mb-1 block">支持证据（每行一条）</label>
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
              <Button size="sm" onclick={addHypothesis}>
                <Check class="h-3.5 w-3.5 mr-1" />
                添加
              </Button>
            </div>
          </div>
        </PopoverContent>
      </Popover>
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

  <!-- 假说内容区域 -->
  {#if hypotheses.length === 0}
    <!-- 无假说时显示空状态卡片 -->
    <div class="bg-card/50 border border-border/50 rounded-lg p-6 text-center shadow-sm" in:fade={{ duration: 200 }}>
      <Lightbulb class="h-10 w-10 mx-auto mb-3 text-yellow-500/50" />
      <h3 class="text-sm font-medium mb-1">暂无假说</h3>
      <p class="text-xs text-muted-foreground mb-4">
        添加假说可以帮助你整理思路和分析事件
      </p>
      <Button variant="outline" size="sm" onclick={() => isAddingHypothesis = true}>
        <Plus class="h-3.5 w-3.5 mr-1" />
        添加第一个假说
      </Button>
    </div>
  {:else if !showDetails}
    <!-- 堆叠卡片视图 -->
    <div class="relative h-[120px] w-full" in:fade={{ duration: 200 }}>
      <!-- 堆叠的卡片 -->
      <div class="absolute inset-0">
        {#each hypotheses.slice(0, 3) as hypothesis, i (hypothesis.id)}
          <div 
            class="absolute inset-0 transition-all duration-300 hover:-translate-y-1 cursor-pointer"
            style={getStackedCardStyle(i, Math.min(hypotheses.length, 3))}
            onclick={() => showDetails = true}
          >
            <TiltedCard
              tiltAngle={getRandomTilt(hypothesis.id, i)}
              bgClass={getRandomBgClass(hypothesis.id)}
              cardClass="px-5 py-4 relative mx-auto rounded-lg shadow-md bg-card dark:bg-card/90 backdrop-blur-xl"
            >
              <div class="flex items-center justify-between">
                <h4 class="font-medium text-sm truncate max-w-[200px]">{hypothesis.title}</h4>
                {#if i === 0}
                  <Badge variant="outline" class="text-xs">
                    {hypotheses.length} 条
                  </Badge>
                {/if}
              </div>
              {#if hypothesis.description && i === 0}
                <p class="text-xs mt-1 line-clamp-2 text-muted-foreground">
                  {hypothesis.description}
                </p>
              {/if}
            </TiltedCard>
          </div>
        {/each}
      </div>
    </div>
  {:else}
    <!-- 详细列表视图 -->
    <ScrollArea class="max-h-[300px] pr-2" in:fade={{ duration: 200 }}>
      <div class="space-y-4">
        {#each hypotheses as hypothesis, index (hypothesis.id)}
          {#if hypothesis.id !== editingHypothesisId}
            <TiltedCard
              tiltAngle={getRandomTilt(hypothesis.id, index)}
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
          {:else}
            <!-- 编辑表单 -->
            <TiltedCard
              tiltAngle={-3}
              bgClass="bg-primary/5 dark:bg-primary/10"
              cardClass="px-6 py-6 relative mx-auto rounded-lg shadow-md bg-card dark:bg-card/90 backdrop-blur-xl"
            >
              <div class="space-y-3">
                <div>
                  <label for="edit-hypothesis-title" class="text-xs font-medium mb-1 block">标题</label>
                  <Input
                    id="edit-hypothesis-title"
                    bind:value={newHypothesisTitle}
                    placeholder="输入假说标题"
                  />
                </div>
                
                <div>
                  <label for="edit-hypothesis-description" class="text-xs font-medium mb-1 block">描述</label>
                  <Textarea
                    id="edit-hypothesis-description"
                    bind:value={newHypothesisDescription}
                    placeholder="描述这个假说的详细内容"
                    rows={2}
                  />
                </div>
                
                <div>
                  <label for="edit-hypothesis-evidence" class="text-xs font-medium mb-1 block">支持证据（每行一条）</label>
                  <Textarea
                    id="edit-hypothesis-evidence"
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
                  <Button size="sm" onclick={saveEditHypothesis}>
                    <Check class="h-3.5 w-3.5 mr-1" />
                    保存
                  </Button>
                </div>
              </div>
            </TiltedCard>
          {/if}
        {/each}
      </div>
    </ScrollArea>
  {/if}
</div>
