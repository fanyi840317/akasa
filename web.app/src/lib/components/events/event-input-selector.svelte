<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import { Button } from '$lib/components/ui/button';
  import { Input } from '$lib/components/ui/input';
  import { Label } from '$lib/components/ui/label';
  import { Textarea } from '$lib/components/ui/textarea';
  import { Loader2 } from 'lucide-svelte';
  import { aiService } from '$lib/services/ai'; // 导入 AI 服务
  import { PUBLIC_GEMINI_API_KEY } from '$env/static/public'; // 导入 API Key

  const dispatch = createEventDispatcher();

  let eventName = $state('');
  let eventUrl = $state('');
  let generatedTitle = $state('');
  let generatedContent = $state('');
  let isLoading = $state(false);
  let error = $state<string | null>(null);
  let mode: 'input' | 'result' = $state('input');

  async function generateFromInput() {
    if (!eventName && !eventUrl) {
      error = '请输入事件名称或提供一个链接。';
      return;
    }
    error = null;
    isLoading = true;
    generatedTitle = '';
    generatedContent = '';

    try {
      // 调用实际的 AI 服务，并传入 API Key
      const result = await aiService.generateEventContent({ 
        apiKey: PUBLIC_GEMINI_API_KEY, 
        name: eventName || undefined, 
        url: eventUrl || undefined 
      });
      generatedTitle = result.title;
      generatedContent = result.content;
      mode = 'result';
    } catch (err: any) {
      console.error('AI 生成失败:', err);
      // 检查 err 是否是 Error 对象并获取 message
      const errorMessage = err instanceof Error ? err.message : String(err);
      error = `无法生成内容：${errorMessage}`; 
    } finally {
      isLoading = false;
    }
  }

  function handleSave() {
    dispatch('save', { title: generatedTitle, content: generatedContent });
    resetState();
  }

  function handleBack() {
    mode = 'input';
    error = null;
  }

  function handleClose() {
    dispatch('close');
    resetState();
  }

  function resetState() {
    eventName = '';
    eventUrl = '';
    generatedTitle = '';
    generatedContent = '';
    isLoading = false;
    error = null;
    mode = 'input';
  }

</script>

<div class="p-4 space-y-4">
  {#if mode === 'input'}
    <h3 class="text-lg font-medium">创建新事件</h3>
    <p class="text-sm text-muted-foreground">输入事件的简要名称或提供相关链接，AI 将尝试生成标题和内容。</p>

    <div class="space-y-2">
      <Label for="event-name">事件名称</Label>
      <Input id="event-name" bind:value={eventName} placeholder="例如：邻居家出现的神秘光球" disabled={isLoading} />
    </div>

    <div class="text-center text-sm text-muted-foreground">或</div>

    <div class="space-y-2">
      <Label for="event-url">相关链接</Label>
      <Input id="event-url" type="url" bind:value={eventUrl} placeholder="例如：https://example.com/news/article" disabled={isLoading} />
    </div>

    {#if error}
      <p class="text-sm text-destructive">{error}</p>
    {/if}

    <div class="flex justify-end space-x-2 pt-4">
      <Button variant="outline" onclick={handleClose} disabled={isLoading}>取消</Button>
      <Button onclick={generateFromInput} disabled={isLoading || (!eventName && !eventUrl)}>
        {#if isLoading}
          <Loader2 class="mr-2 h-4 w-4 animate-spin" />
        {/if}
        生成内容
      </Button>
    </div>

  {:else if mode === 'result'}
    <h3 class="text-lg font-medium">AI 生成结果</h3>
    <p class="text-sm text-muted-foreground">请检查 AI 生成的标题和内容，您可以修改后保存。</p>

    <div class="space-y-2">
      <Label for="generated-title">标题</Label>
      <Input id="generated-title" bind:value={generatedTitle} />
    </div>

    <div class="space-y-2">
      <Label for="generated-content">内容摘要</Label>
      <Textarea id="generated-content" bind:value={generatedContent} rows={5} />
    </div>

    <div class="flex justify-end space-x-2 pt-4">
       <Button variant="outline" onclick={handleBack}>返回修改</Button>
      <Button onclick={handleSave}>保存事件</Button>
    </div>
  {/if}
</div>