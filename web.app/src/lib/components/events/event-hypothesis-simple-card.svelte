<script lang="ts">
  import { cn } from "$lib/utils";
  import { Button } from "$lib/components/ui/button";
  import { Plus, Edit2, Trash2 } from "lucide-svelte";
  import { ScrollArea } from "$lib/components/ui/scroll-area";
  import type { Hypothesis } from "$lib/types/timeline";
  import { createEventDispatcher } from "svelte";

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
  let isAddingHypothesis = $state(false);
  let editingHypothesisId = $state<string | null>(null);
  let newHypothesisTitle = $state("");
  let newHypothesisDescription = $state("");

  // 添加新假说
  function addHypothesis() {
    if (!newHypothesisTitle.trim()) return;

    const newHypothesis: Hypothesis = {
      id: crypto.randomUUID(),
      title: newHypothesisTitle.trim(),
      description: newHypothesisDescription.trim(),
      evidence: [],
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
  }
</script>

<div class={cn("w-full px-4 py-3", className)}>
  <div class="flex justify-between items-center mb-2">
    <h3 class="text-xl font-bold text-gray-900 dark:text-gray-100">
      假说
    </h3>
    {#if !isAddingHypothesis && !editingHypothesisId}
      <Button variant="ghost" size="sm" class="h-7 w-7 p-0" onclick={() => isAddingHypothesis = true}>
        <Plus class="h-4 w-4" />
      </Button>
    {/if}
  </div>
  <p class="text-gray-700 dark:text-gray-400 text-sm mb-3">创建和管理事件的假说和理论</p>

  <ScrollArea class="h-[120px] pr-2">
    {#if isAddingHypothesis || editingHypothesisId}
      <div class="bg-muted/50 p-3 rounded-lg space-y-2 mb-3">
        <input
          type="text"
          bind:value={newHypothesisTitle}
          placeholder="假说标题"
          class="w-full px-3 py-1.5 text-sm rounded-md border border-input bg-background"
        />
        <textarea
          bind:value={newHypothesisDescription}
          placeholder="假说描述"
          rows="2"
          class="w-full px-3 py-1.5 text-sm rounded-md border border-input bg-background"
        ></textarea>
        <div class="flex justify-end gap-2">
          <Button variant="outline" size="sm" onclick={resetForm}>取消</Button>
          <Button size="sm" onclick={editingHypothesisId ? saveEditHypothesis : addHypothesis}>
            {editingHypothesisId ? '保存' : '添加'}
          </Button>
        </div>
      </div>
    {/if}

    {#if hypotheses.length === 0 && !isAddingHypothesis}
      <div class="text-center py-4 text-muted-foreground">
        <p>暂无假说</p>
        <p class="text-xs mt-1">点击右上角的加号添加假说</p>
      </div>
    {:else}
      {#each hypotheses as hypothesis}
        {#if hypothesis.id !== editingHypothesisId}
          <div class="bg-card border rounded-lg p-3 shadow-sm mb-2">
            <div class="flex justify-between items-start">
              <h4 class="font-medium text-sm">{hypothesis.title}</h4>
              <div class="flex gap-1">
                <Button variant="ghost" size="icon" class="h-6 w-6" onclick={() => startEditHypothesis(hypothesis)}>
                  <Edit2 class="h-3 w-3" />
                </Button>
                <Button variant="ghost" size="icon" class="h-6 w-6 text-destructive" onclick={() => deleteHypothesis(hypothesis.id)}>
                  <Trash2 class="h-3 w-3" />
                </Button>
              </div>
            </div>
            {#if hypothesis.description}
              <p class="text-xs text-muted-foreground mt-1">{hypothesis.description}</p>
            {/if}
          </div>
        {/if}
      {/each}
    {/if}
  </ScrollArea>
</div>
