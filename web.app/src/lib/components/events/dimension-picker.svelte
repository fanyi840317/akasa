<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import { Input } from "$lib/components/ui/input";
  import { Textarea } from "$lib/components/ui/textarea";
  import { Plus, X, FileText } from "lucide-svelte";
  import * as Dialog from "$lib/components/ui/dialog";
  import { ScrollArea } from "$lib/components/ui/scroll-area";

  // 定义维度类型
  type Dimension = {
    title: string;
    questions: string[];
    findings: string[];
    hypotheses: string[];
  };

  let { 
    dimensions = [],
    onDimensionsChange = (dimensions: Dimension[]) => {}
  } = $props<{
    dimensions?: Dimension[];
    onDimensionsChange?: (dimensions: Dimension[]) => void;
  }>();

  // 维度管理
  let showDimensionEditor = $state(false);
  let editingDimension: Dimension | null = null;
  let dimensionTitle = "";
  let dimensionQuestions = "";
  let dimensionFindings = "";
  let dimensionHypotheses = "";
  
  function openDimensionEditor(dimension?: Dimension) {
    if (dimension) {
      editingDimension = dimension;
      dimensionTitle = dimension.title;
      dimensionQuestions = dimension.questions.join("\n");
      dimensionFindings = dimension.findings.join("\n");
      dimensionHypotheses = dimension.hypotheses.join("\n");
    } else {
      editingDimension = null;
      dimensionTitle = "";
      dimensionQuestions = "";
      dimensionFindings = "";
      dimensionHypotheses = "";
    }
    showDimensionEditor = true;
  }
  
  function saveDimension() {
    if (!dimensionTitle.trim()) return;
    
    const newDimension: Dimension = {
      title: dimensionTitle.trim(),
      questions: dimensionQuestions.split("\n").filter(q => q.trim()),
      findings: dimensionFindings.split("\n").filter(f => f.trim()),
      hypotheses: dimensionHypotheses.split("\n").filter(h => h.trim())
    };
    
    let updatedDimensions;
    if (editingDimension) {
      // 更新现有维度
      updatedDimensions = dimensions.map((d: Dimension) => 
        d === editingDimension ? newDimension : d
      );
    } else {
      // 添加新维度
      updatedDimensions = [...dimensions, newDimension];
    }
    
    onDimensionsChange(updatedDimensions);
    showDimensionEditor = false;
  }
  
  function deleteDimension(dimension: Dimension) {
    const updatedDimensions = dimensions.filter((d: Dimension) => d !== dimension);
    onDimensionsChange(updatedDimensions);
  }
</script>

<div class="w-full">
  <div class="flex flex-col items-end gap-1">
    <span class="text-xs text-muted-foreground">维度列表</span>
    <div class="w-full">
      {#if dimensions.length === 0}
        <div class="text-xs text-muted-foreground text-center w-full py-2 border border-dashed border-border/40 rounded-md">
          暂无维度数据
        </div>
      {:else}
        <ScrollArea class="h-[200px] w-full">
          <div class="space-y-2 w-full pr-2">
            {#each dimensions as dimension}
              <div class="border border-border/40 rounded-md p-2 text-xs hover:bg-muted/50 transition-colors">
                <div class="flex justify-between items-center">
                  <span class="font-medium">{dimension.title}</span>
                  <div class="flex gap-1">
                    <Button variant="ghost" size="sm" class="h-5 w-5 p-0" onclick={() => openDimensionEditor(dimension)}>
                      <FileText class="h-3 w-3" />
                    </Button>
                    <Button variant="ghost" size="sm" class="h-5 w-5 p-0" onclick={() => deleteDimension(dimension)}>
                      <X class="h-3 w-3" />
                    </Button>
                  </div>
                </div>
                <div class="mt-1 text-muted-foreground">
                  {dimension.questions.length} 个问题 · {dimension.findings.length} 个发现 · {dimension.hypotheses.length} 个假设
                </div>
              </div>
            {/each}
          </div>
        </ScrollArea>
      {/if}
      
      <div class="flex justify-end mt-2">
        <Button variant="ghost" size="sm" class="h-6 w-6 p-0" onclick={() => openDimensionEditor()}>
          <Plus class="h-4 w-4" />
        </Button>
      </div>
    </div>
  </div>
</div>

<!-- 维度编辑器弹窗 -->
<Dialog.Root bind:open={showDimensionEditor}>
  <Dialog.Content class="sm:max-w-[500px]">
    <Dialog.Header>
      <Dialog.Title>{editingDimension ? '编辑维度' : '添加维度'}</Dialog.Title>
    </Dialog.Header>
    
    <div class="space-y-4 py-4">
      <div>
        <label class="text-sm font-medium">维度标题</label>
        <Input bind:value={dimensionTitle} placeholder="例如：历史考古" />
      </div>
      
      <div>
        <label class="text-sm font-medium">问题（每行一个）</label>
        <Textarea bind:value={dimensionQuestions} placeholder="是否存在与巴别塔相关的实际遗迹？" rows={3} />
      </div>
      
      <div>
        <label class="text-sm font-medium">发现（每行一个）</label>
        <Textarea bind:value={dimensionFindings} placeholder="古巴比伦的宗教塔（如Etemenanki）可能是巴别塔原型" rows={3} />
      </div>
      
      <div>
        <label class="text-sm font-medium">假设（每行一个）</label>
        <Textarea bind:value={dimensionHypotheses} placeholder="圣经故事基于真实历史建筑，但被后人神话化" rows={3} />
      </div>
    </div>
    
    <Dialog.Footer>
      <Button variant="outline" onclick={() => showDimensionEditor = false}>取消</Button>
      <Button onclick={saveDimension}>保存</Button>
    </Dialog.Footer>
  </Dialog.Content>
</Dialog.Root> 