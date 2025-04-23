<script lang="ts">
  import { cn } from "$lib/utils";
  import { Button } from "$lib/components/ui/button";
  import { Plus, Edit2, Trash2, Lightbulb, ChevronDown, ChevronUp, Check, X } from "lucide-svelte";
  import { ScrollArea } from "$lib/components/ui/scroll-area";
  import type { Hypothesis } from "$lib/types/timeline";
  import { createEventDispatcher } from "svelte";
  import { fade, fly, slide } from "svelte/transition";
  import { Input } from "$lib/components/ui/input";
  import { Textarea } from "$lib/components/ui/textarea";
  import { Badge } from "$lib/components/ui/badge";

  // 创建事件分发器
  const dispatch = createEventDispatcher<{
    hypothesisChange: { hypotheses: Hypothesis[] };
  }>();

  // 组件属性
  let {
    hypotheses = $bindable([]),
    className = "",
  } = $props<{
    hypotheses: Hypothesis[];
    class?: string;
  }>();

  // 导出 class
  export { className as class };

  // 状态变量
  let isExpanded = $state(false);
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
      evidence: newHypothesisEvidence.trim() ? newHypothesisEvidence.split('\n').map(e => e.trim()).filter(Boolean) : [],
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
    newHypothesisEvidence = hypothesis.evidence.join('\n');
  }

  // 保存编辑的假说
  function saveEditHypothesis() {
    if (!newHypothesisTitle.trim()) return;

    hypotheses = hypotheses.map(h => {
      if (h.id === editingHypothesisId) {
        return {
          ...h,
          title: newHypothesisTitle.trim(),
          description: newHypothesisDescription.trim(),
          evidence: newHypothesisEvidence.trim() ? newHypothesisEvidence.split('\n').map(e => e.trim()).filter(Boolean) : [],
        };
      }
      return h;
    });

    resetForm();
    dispatch("hypothesisChange", { hypotheses });
  }

  // 删除假说
  function deleteHypothesis(id: string) {
    hypotheses = hypotheses.filter(h => h.id !== id);
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

  // 切换展开/折叠状态
  function toggleExpand() {
    isExpanded = !isExpanded;
  }

  // 切换假说展开/折叠状态
  function toggleHypothesisExpand(id: string) {
    expandedHypothesisId = expandedHypothesisId === id ? null : id;
  }

  // 格式化日期
  function formatDate(date: Date): string {
    return date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
    });
  }

  // 获取随机颜色
  function getRandomColor(id: string): string {
    const colors = [
      'bg-blue-100 border-blue-300 text-blue-800',
      'bg-green-100 border-green-300 text-green-800',
      'bg-yellow-100 border-yellow-300 text-yellow-800',
      'bg-purple-100 border-purple-300 text-purple-800',
      'bg-pink-100 border-pink-300 text-pink-800',
      'bg-indigo-100 border-indigo-300 text-indigo-800',
    ];
    
    // 使用ID的哈希值来确定颜色，这样同一个假说总是有相同的颜色
    const hash = id.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
    return colors[hash % colors.length];
  }
</script>

<div class={cn("w-full px-4 py-3 relative", className)}>
  <!-- 标题栏 -->
  <div 
    class="flex justify-between items-center mb-2 cursor-pointer" 
    onclick={toggleExpand}
  >
    <div class="flex items-center gap-2">
      <Lightbulb class="h-5 w-5 text-yellow-500" />
      <h3 class="text-lg font-bold text-gray-900 dark:text-gray-100">
        假说与理论
      </h3>
      {#if hypotheses.length > 0}
        <Badge variant="outline" class="ml-2">{hypotheses.length}</Badge>
      {/if}
    </div>
    <div class="flex items-center">
      {#if !isAddingHypothesis && !editingHypothesisId && !isExpanded}
        <Button variant="ghost" size="sm" class="h-7 w-7 p-0 mr-1" onclick={(e) => {
          e.stopPropagation();
          isAddingHypothesis = true;
          isExpanded = true;
        }}>
          <Plus class="h-4 w-4" />
        </Button>
      {/if}
      <Button variant="ghost" size="sm" class="h-7 w-7 p-0" onclick={(e) => {
        e.stopPropagation();
        toggleExpand();
      }}>
        {#if isExpanded}
          <ChevronUp class="h-4 w-4" />
        {:else}
          <ChevronDown class="h-4 w-4" />
        {/if}
      </Button>
    </div>
  </div>

  <!-- 展开内容 -->
  {#if isExpanded}
    <div in:slide={{ duration: 300 }} out:slide={{ duration: 300 }}>
      <!-- 添加/编辑表单 -->
      {#if isAddingHypothesis || editingHypothesisId}
        <div 
          class="bg-muted/30 p-4 rounded-lg space-y-3 mb-4 border border-muted-foreground/20 shadow-sm"
          in:fly={{ y: -10, duration: 200 }}
        >
          <div>
            <label for="hypothesis-title" class="text-xs font-medium mb-1 block">标题</label>
            <Input id="hypothesis-title" bind:value={newHypothesisTitle} placeholder="输入假说标题" />
          </div>
          
          <div>
            <label for="hypothesis-description" class="text-xs font-medium mb-1 block">描述</label>
            <Textarea id="hypothesis-description" bind:value={newHypothesisDescription} placeholder="描述这个假说的详细内容" rows={2} />
          </div>
          
          <div>
            <label for="hypothesis-evidence" class="text-xs font-medium mb-1 block">支持证据（每行一条）</label>
            <Textarea id="hypothesis-evidence" bind:value={newHypothesisEvidence} placeholder="列出支持这个假说的证据" rows={3} />
          </div>
          
          <div class="flex justify-end gap-2 pt-2">
            <Button variant="outline" size="sm" onclick={resetForm}>
              <X class="h-3.5 w-3.5 mr-1" />
              取消
            </Button>
            <Button size="sm" onclick={editingHypothesisId ? saveEditHypothesis : addHypothesis}>
              <Check class="h-3.5 w-3.5 mr-1" />
              {editingHypothesisId ? '保存' : '添加'}
            </Button>
          </div>
        </div>
      {/if}

      <!-- 假说列表 -->
      <ScrollArea class="max-h-[240px] pr-2">
        {#if hypotheses.length === 0 && !isAddingHypothesis}
          <div class="text-center py-6 text-muted-foreground">
            <Lightbulb class="h-8 w-8 mx-auto mb-2 opacity-50" />
            <p>暂无假说</p>
            <p class="text-xs mt-1">点击右上角的加号添加假说</p>
          </div>
        {:else}
          <div class="space-y-3">
            {#each hypotheses as hypothesis}
              {#if hypothesis.id !== editingHypothesisId}
                <div 
                  class={cn("rounded-lg p-3 border shadow-sm transition-all duration-200 hover:shadow-md", getRandomColor(hypothesis.id))}
                  in:fade={{ duration: 200 }}
                >
                  <div class="flex justify-between items-start">
                    <div 
                      class="flex-1 cursor-pointer" 
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
                        <p class="text-xs mt-1 line-clamp-1">{hypothesis.description}</p>
                      {/if}
                    </div>
                    
                    <div class="flex gap-1 ml-2">
                      <Button variant="ghost" size="icon" class="h-6 w-6 bg-white/40" onclick={() => startEditHypothesis(hypothesis)}>
                        <Edit2 class="h-3 w-3" />
                      </Button>
                      <Button variant="ghost" size="icon" class="h-6 w-6 bg-white/40 text-red-600" onclick={() => deleteHypothesis(hypothesis.id)}>
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
                        <div class="mt-2 bg-white/50 p-2 rounded">
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
                </div>
              {/if}
            {/each}
          </div>
        {/if}
      </ScrollArea>
    </div>
  {:else if hypotheses.length > 0}
    <!-- 折叠状态下的预览 -->
    <div class="flex gap-2 overflow-x-auto py-1 pb-2 no-scrollbar">
      {#each hypotheses.slice(0, 3) as hypothesis}
        <div 
          class={cn("rounded-lg p-2 border shadow-sm flex-shrink-0 max-w-[180px] cursor-pointer", getRandomColor(hypothesis.id))}
          onclick={() => {
            isExpanded = true;
            expandedHypothesisId = hypothesis.id;
          }}
        >
          <h4 class="font-medium text-xs truncate">{hypothesis.title}</h4>
          {#if hypothesis.description}
            <p class="text-xs mt-1 line-clamp-1">{hypothesis.description}</p>
          {/if}
        </div>
      {/each}
      {#if hypotheses.length > 3}
        <div 
          class="rounded-lg p-2 border shadow-sm flex-shrink-0 bg-muted/30 flex items-center justify-center cursor-pointer min-w-[60px]"
          onclick={() => isExpanded = true}
        >
          <span class="text-xs">+{hypotheses.length - 3} 更多</span>
        </div>
      {/if}
    </div>
  {/if}
</div>

<style>
  .no-scrollbar {
    -ms-overflow-style: none;  /* IE and Edge */
    scrollbar-width: none;  /* Firefox */
  }
  .no-scrollbar::-webkit-scrollbar {
    display: none;  /* Chrome, Safari and Opera */
  }
</style>
