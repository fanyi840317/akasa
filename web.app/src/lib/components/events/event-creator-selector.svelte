<script lang="ts">
  import * as Modal from "$lib/components/ui/modal";
  import { Button } from "$lib/components/ui/button";
  import { Eye, FileText, Camera, UserCircle2, X } from "lucide-svelte";
  import { createEventDispatcher } from "svelte";
  import { fade, fly, scale, slide } from 'svelte/transition';
  import { elasticOut, backOut, cubicOut } from 'svelte/easing';

  let { open = false } = $props();

  const dispatch = createEventDispatcher<{
    select: { type: "experience" | "documentation" | "witness" | "evidence" };
    close: void;
  }>();

  function handleSelect(type: "experience" | "documentation" | "witness" | "evidence") {
    dispatch("select", { type });
    open = false;
  }

  function handleClose() {
    open = false;
    dispatch("close");
  }

  // 动画配置
  const backdropTransition = { duration: 200 };
  const modalTransition = { duration: 300, y: 20 };
</script>

{#if open}
  <div 
    class="fixed inset-0 z-50 bg-neutral-900/10 backdrop-blur-[2px] dark:bg-neutral-900/50" 
    on:click|self={handleClose}
    in:fade={backdropTransition}
    out:fade={backdropTransition}
  >
    <div 
      class="fixed left-[50%] top-[50%] z-50 w-full max-w-2xl translate-x-[-50%] translate-y-[-50%] overflow-hidden"
      in:fly={modalTransition}
      out:fade={{ duration: 150 }}
    >
      <div class="flex justify-between items-center p-4">
        <div>
          <h3 class="text-lg font-semibold">选择分享类型</h3>
          <p class="text-sm text-muted-foreground">选择最适合你要分享内容的类型，这将帮助我们提供更好的录入表单</p>
        </div>
        <button class="rounded-sm opacity-70 hover:opacity-100 focus:outline-none" on:click={handleClose}>
          <X class="h-4 w-4" />
        </button>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 p-4">
        <!-- 卡片1：分享亲身经历 -->
        <div in:fly={{ x: -20, duration: 300, delay: 100, easing: cubicOut }}>
          <Button
            variant="outline"
            class="h-auto p-6 w-full flex flex-col items-start gap-2 bg-neutral-900 hover:bg-muted/50 transition-colors "
            onclick={() => handleSelect("experience")}
          >
            <div class="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
              <UserCircle2 class="w-6 h-6 text-primary" />
            </div>
            <div class="text-left">
              <h3 class="font-medium">分享我的亲身经历</h3>
              <p class="text-sm text-muted-foreground">记录下你亲身经历过的无法解释的事件</p>
            </div>
          </Button>
        </div>
        
        <!-- 卡片2：整理公众事件 -->
        <div in:fly={{ x: 20, duration: 300, delay: 150, easing: cubicOut }}>
          <Button
            variant="outline"
            class="h-auto p-6 w-full flex flex-col items-start gap-2 bg-neutral-900 rounded-lg hover:bg-muted/50 transition-colors"
            onclick={() => handleSelect("documentation")}
          >
            <div class="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
              <FileText class="w-6 h-6 text-primary" />
            </div>
            <div class="text-left">
              <h3 class="font-medium">整理已知的公众事件</h3>
              <p class="text-sm text-muted-foreground">帮助完善已知神秘事件的档案记录</p>
            </div>
          </Button>
        </div>
        
        <!-- 卡片3：目击者/知情人 -->
        <div in:scale={{ duration: 300, delay: 200, start: 0.9, opacity: 0, easing: backOut }}>
          <Button
            variant="outline"
            class="h-auto p-6 w-full flex flex-col items-start gap-2 hover:bg-muted/50 transition-colors"
            onclick={() => handleSelect("witness")}
          >
            <div class="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
              <Eye class="w-6 h-6 text-primary" />
            </div>
            <div class="text-left">
              <h3 class="font-medium">我是目击者/知情人</h3>
              <p class="text-sm text-muted-foreground">分享你所目击或了解的关键信息</p>
            </div>
          </Button>
        </div>
        
        <!-- 卡片4：证据/线索 -->
        <div in:scale={{ duration: 300, delay: 250, start: 0.9, opacity: 0, easing: backOut }}>
          <Button
            variant="outline"
            class="h-auto p-6 w-full flex flex-col items-start gap-2 hover:bg-muted/50 transition-colors"
            onclick={() => handleSelect("evidence")}
          >
            <div class="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
              <Camera class="w-6 h-6 text-primary" />
            </div>
            <div class="text-left">
              <h3 class="font-medium">我有证据/线索</h3>
              <p class="text-sm text-muted-foreground">提交照片、视频等相关证据</p>
            </div>
          </Button>
        </div>
      </div>
    </div>
  </div>
{/if} 