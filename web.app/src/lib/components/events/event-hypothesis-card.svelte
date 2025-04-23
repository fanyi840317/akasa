<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import { Plus, X, Check, Edit2, Trash2 } from "lucide-svelte";
  import { Button } from "$lib/components/ui/button";
  import { Input } from "$lib/components/ui/input";
  import { Textarea } from "$lib/components/ui/textarea";
  import { Badge } from "$lib/components/ui/badge";
  import { ScrollArea } from "$lib/components/ui/scroll-area";
  import type { Hypothesis } from "$lib/types/timeline";
  import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "$lib/components/ui/card";
  import { toast } from "svelte-sonner";

  // 创建事件分发器
  const dispatch = createEventDispatcher<{
    hypothesisChange: { hypotheses: Hypothesis[] };
  }>();

  // 组件属性
  let {
    hypotheses = $bindable([]),
  } = $props<{
    hypotheses: Hypothesis[];
  }>();

  // 状态变量
  let isAddingHypothesis = $state(false);
  let editingHypothesisId = $state<string | null>(null);
  let newHypothesisTitle = $state("");
  let newHypothesisDescription = $state("");
  let newHypothesisEvidence = $state("");

  // 添加新假说
  function addHypothesis() {
    if (!newHypothesisTitle.trim()) {
      toast.error("请输入假说标题");
      return;
    }

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
    if (!newHypothesisTitle.trim()) {
      toast.error("请输入假说标题");
      return;
    }

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

  // 格式化日期
  function formatDate(date: Date): string {
    return date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
    });
  }
</script>

<Card class="w-full h-full border-0 shadow-none">
  <CardHeader class="pb-2">
    <div class="flex justify-between items-center">
      <CardTitle class="text-lg font-semibold">假说</CardTitle>
      {#if !isAddingHypothesis && !editingHypothesisId}
        <Button variant="ghost" size="sm" class="h-8 w-8 p-0" onclick={() => isAddingHypothesis = true}>
          <Plus class="h-4 w-4" />
        </Button>
      {/if}
    </div>
    <CardDescription>
      创建和管理事件的假说和理论
    </CardDescription>
  </CardHeader>

  <CardContent class="p-0">
    <ScrollArea class="h-[calc(100vh-280px)]">
      <div class="px-4 py-2 space-y-4">
        <!-- 添加/编辑假说表单 -->
        {#if isAddingHypothesis || editingHypothesisId}
          <div class="bg-muted/50 p-3 rounded-lg space-y-3">
            <div>
              <label for="hypothesis-title" class="text-xs font-medium mb-1 block">标题</label>
              <Input id="hypothesis-title" bind:value={newHypothesisTitle} placeholder="输入假说标题" />
            </div>
            
            <div>
              <label for="hypothesis-description" class="text-xs font-medium mb-1 block">描述</label>
              <Textarea id="hypothesis-description" bind:value={newHypothesisDescription} placeholder="描述这个假说的详细内容" rows={3} />
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
        {#if hypotheses.length === 0 && !isAddingHypothesis}
          <div class="text-center py-8 text-muted-foreground">
            <p>暂无假说</p>
            <p class="text-xs mt-1">点击右上角的加号添加假说</p>
          </div>
        {:else}
          {#each hypotheses as hypothesis}
            {#if hypothesis.id !== editingHypothesisId}
              <div class="bg-card border rounded-lg p-3 shadow-sm">
                <div class="flex justify-between items-start">
                  <h3 class="font-medium text-sm">{hypothesis.title}</h3>
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
                
                {#if hypothesis.evidence.length > 0}
                  <div class="mt-2">
                    <h4 class="text-xs font-medium mb-1">支持证据:</h4>
                    <ul class="text-xs space-y-1 pl-4 list-disc">
                      {#each hypothesis.evidence as evidence}
                        <li>{evidence}</li>
                      {/each}
                    </ul>
                  </div>
                {/if}
                
                <div class="mt-2 text-xs text-muted-foreground">
                  创建于: {formatDate(hypothesis.createdAt)}
                </div>
              </div>
            {/if}
          {/each}
        {/if}
      </div>
    </ScrollArea>
  </CardContent>
</Card>
