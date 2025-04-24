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
    import Meteors from "../ui/background/meteors.svelte";
    import ShineBorder from "../ui/background/shine-border.svelte";
    import { Card } from "../ui/card";

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
    // 向上堆叠，所以偏移量为负值
    const offset = -((index / (total - 1)) * maxOffset);
    const rotate = ((index / (total - 1)) * 2 - 1) * maxRotate;

    return `transform: translateY(${offset}px) rotate(${rotate}deg); z-index: ${100 - index};`;
  }
</script>

<div class={cn("w-full py-3 relative", className)}>
  <Card class="dark:bg-neutral-900 w-full h-[220px] text-center" color="white">
      
    
  </Card>
</div>
