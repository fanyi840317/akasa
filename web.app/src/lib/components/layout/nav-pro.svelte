<script lang="ts">
  import * as Sidebar from "$lib/components/ui/sidebar/index.js";
  import File from "@lucide/svelte/icons/file";
  import Folder from "@lucide/svelte/icons/folder";
  import { onMount, onDestroy, type ComponentProps } from "svelte";
  import { Button } from "$lib/components/ui/button";
  import * as Card from "$lib/components/ui/card";
  import { Ellipsis, Forward, Plus, Trash2, Sparkles, BookOpen, Link, FilePlus, FileText } from "lucide-svelte"; // Import new icons
  import AiEventCreatorModal from "$lib/components/events/ai-event-creator-modal.svelte"; // Import the new modal
  import { auth } from "$lib/stores/auth";
  import { get } from "svelte/store";
  import { eventStore } from "$lib/stores/event";
  import { Skeleton } from "$lib/components/ui/skeleton";
  import * as DropdownMenu from "$lib/components/ui/dropdown-menu";
  // Popover import removed as it's no longer used here
  import { useSidebar } from "$lib/components/ui/sidebar/index.js";
  import { page } from "$app/stores";
  import { appStore } from "$lib/stores/appState";
  import type { Event } from "$lib/types/event";
  import { goto } from '$app/navigation';
  import { createDocByMarkdown, exportDocToJson } from "$lib/components/editor/affine-editor";
  import { Job } from "@blocksuite/store";


  // 组件属性
  let {
    ref = $bindable(null),
    ...restProps
  }: ComponentProps<typeof Sidebar.Root> = $props();

  // 获取侧边栏实例
  const sidebar = useSidebar();

  // 状态
  let showAiCreatorModal = $state(false); // State for the new AI creator modal

  // 从 eventStore 获取状态
  let userEvents: Event[] = $state([]);
  let hasEvents = $state(false);
  let isLoading = $state(false);

  // 事件处理函数
  function openAiEventCreator() {
    showAiCreatorModal = true;
  }


  async function handleAiEventSave(event: CustomEvent<{
    title: string;
    content: string;
    eventTime?: string;
    entities?: any;
    primaryLocation?: any;
  }>) {
    const { title, content, eventTime, entities, primaryLocation } = event.detail;
    console.log('保存 AI 生成的事件:', { title, content, eventTime, entities, primaryLocation });

    try {
      // 使用 createDocByMarkdown 处理 markdown 格式的内容
      const doc = await createDocByMarkdown(content, title);
      if (!doc) {
        console.error('创建文档失败');
        return;
      }

      // 使用 exportDocToJson 将文档转换为 JSON 格式
      const jsonData = await exportDocToJson(doc);
      if (!jsonData) {
        console.error('导出文档为 JSON 失败');
        return;
      }

      // 构建完整的 Event 对象，使用 JSON 格式的内容
      const eventData = {
        title: title,
        content: jsonData.content, // 使用 JSON 格式的内容
        // 转换位置数据为 Location 类型
        location_data: primaryLocation ? {
          address: primaryLocation.name,
          description: primaryLocation.description,
          latitude: primaryLocation.coordinates?.[0],
          longitude: primaryLocation.coordinates?.[1]
        } : entities?.locations?.[0] ? {
          address: entities.locations[0].name,
          description: entities.locations[0].description,
          latitude: entities.locations[0].coordinates?.[0],
          longitude: entities.locations[0].coordinates?.[1]
        } : undefined,
        // location_data: entities?.locations ? JSON.stringify(entities.locations) : undefined,
        date: eventTime || entities?.timeline?.[0]?.time || new Date().toISOString(),
        status: 'draft',
        privacy: 'private',
        entities_data: JSON.stringify(entities ? entities : undefined),
        user_id: get(auth).user?.$id ?? ''
      };

      eventStore.createEvent(eventData)
        .then((newEvent) => {
          eventStore.fetchEvents(); // 刷新列表
          if (newEvent && newEvent.$id) {
             goto(`/console/events/${newEvent.$id}`); // Navigate to the newly created event
          }
          showAiCreatorModal = false;
        })
        .catch(error => {
          console.error('创建事件失败:', error);
        });
    } catch (error) {
      console.error('处理 Markdown 内容失败:', error);
    }
  }

  type EventType = "experience" | "documentation" | "witness" | "evidence";

  async function handleImportMarkdown(event: any) {
    const fileInput = event.target as HTMLInputElement;
    if (!fileInput.files || fileInput.files.length === 0) return;

    const file = fileInput.files[0];
    const reader = new FileReader();

    reader.onload = async (e) => {
      try {
        const markdown = e.target?.result as string;
        if (!markdown) return;

        // 从文件名中提取标题（去掉扩展名）
        const title = file.name.replace(/\.md$|\.markdown$/i, '');

        // 使用 createDocByMarkdown 创建文档
        const doc = await createDocByMarkdown(markdown, title);
        if (!doc) {
          console.error('创建文档失败');
          return;
        }

        // 使用 exportDocToJson 导出为 JSON
        const jsonData = await exportDocToJson(doc);
        if (!jsonData) {
          console.error('导出文档为 JSON 失败');
          return;
        }

        // 构建事件数据
        const eventData = {
          title: title,
          content: jsonData.content,
          date: new Date().toISOString(),
          status: 'draft',
          privacy: 'private',
          user_id: get(auth).user?.$id ?? ''
        };

        // 保存事件
        eventStore.createEvent(eventData)
          .then((newEvent) => {
            eventStore.fetchEvents(); // 刷新列表
            if (newEvent && newEvent.$id) {
              goto(`/console/events/${newEvent.$id}`); // 导航到新创建的事件
            }
          })
          .catch(error => {
            console.error('创建事件失败:', error);
          });
      } catch (error) {
        console.error('处理Markdown文件失败:', error);
      }
    };

    reader.readAsText(file);

    // 重置文件输入，以便可以再次选择同一文件
    fileInput.value = '';
  }

  function handleEventSelect(eventId: string) {
    goto(`/console/events/${eventId}`);
  }

  function handleEventDelete(eventId: string) {
    // 检查当前页面是否是正在被删除的事件页面
    const isCurrentEvent = isEventActive(eventId);

    // 删除事件
    eventStore.deleteEvent(eventId)
      .then(() => {
        // 如果当前页面是正在被删除的事件页面，则导航到主页面
        if (isCurrentEvent) {
          goto('/console/events');
        }
      })
      .catch(error => {
        console.error('删除事件失败:', error);
      });
  }

  // 判断事件是否激活
  function isEventActive(eventId: string): boolean {
    const pathname = $page.url.pathname;
    return pathname === `/console/events/${eventId}`;
  }

  // Store 订阅
  const unsubscribe = eventStore.subscribe((state) => {
    userEvents = state.events;
    hasEvents = state.events.length > 0;
    isLoading = state.listLoading;
  });

  // 生命周期钩子
  onMount(async () => {
    const userId = get(auth).user?.$id;
    if (userId) {
      try {
        await eventStore.fetchEvents(userId);
      } catch (error) {
        console.error('获取用户事件失败:', error);
      }
    }
  });

  onDestroy(() => {
    unsubscribe();
  });
</script>


<AiEventCreatorModal
  bind:open={showAiCreatorModal}
  onSave={(data) => handleAiEventSave(new CustomEvent('save', { detail: data }))}
/>

<Sidebar.Group>
  {#if isLoading}
    <div class="flex items-center space-x-4 p-4">
      <div class="space-y-2 flex-1">
        <Skeleton class="h-4 w-[80%]" />
        <Skeleton class="h-3 w-[60%]" />
        <Skeleton class="h-4 w-[80%]" />
        <Skeleton class="h-3 w-[60%]" />
      </div>
    </div>
  {:else if !hasEvents}
  <Card.Root class="shadow-none bg-muted/10 border-primary/10">
    <form>
      <Card.Header class="p-4 pb-0">
        <Card.Title class="text-sm  text-primary/70">探索未知的世界</Card.Title>
        <Card.Description class="text-xs">
          每一个神秘事件背后都有一个等待被讲述的故事，分享你的发现
        </Card.Description>
      </Card.Header>
      <Card.Content class="grid px-2 py-4">
        <Button
          variant="outline"
          class="w-full "
          size="sm"
          onclick={openAiEventCreator}
        >
          <Sparkles class="mr-2 h-4 w-4" />
          我要爆料
        </Button>
      </Card.Content>
    </form>
  </Card.Root>
  {:else}
  <Sidebar.GroupLabel>私人</Sidebar.GroupLabel>
    <!-- Use DropdownMenu for adding events -->
    <DropdownMenu.Root>
      <DropdownMenu.Trigger>
        <Sidebar.GroupAction
          title="添加事件"
        >
          <Plus /> <span class="sr-only">添加事件</span>
        </Sidebar.GroupAction>
      </DropdownMenu.Trigger>
      <DropdownMenu.Content class="w-48 p-1" side="right" align="start">
        <DropdownMenu.Item onclick={openAiEventCreator}>
          <Sparkles class="mr-2 h-4 w-4 text-muted-foreground" />
          用AI创建
        </DropdownMenu.Item>
        <DropdownMenu.Item onclick={() => appStore.openEventCreator('documentation')}>
          <FilePlus class="mr-2 h-4 w-4 text-muted-foreground" />
          全新创建
        </DropdownMenu.Item>
        <DropdownMenu.Separator />
        <DropdownMenu.Item onclick={() => document.getElementById('markdown-file-input')?.click()}>
          <FileText class="mr-2 h-4 w-4 text-muted-foreground" />
          导入Markdown
        </DropdownMenu.Item>
        <input
          type="file"
          id="markdown-file-input"
          accept=".md,.markdown,text/markdown"
          class="hidden"
          onchange={handleImportMarkdown}
        />
      </DropdownMenu.Content>
    </DropdownMenu.Root>

    <Sidebar.GroupContent>
      <Sidebar.Menu>
        {#each userEvents as event}
          {@render events({ id: event.$id ?? '', title: event.title ?? '' })}
        {/each}
      </Sidebar.Menu>
    </Sidebar.GroupContent>
  {/if}
</Sidebar.Group>

{#snippet events({ id, title }: { id: string; title: string })}
  <Sidebar.MenuItem>
    <Sidebar.MenuButton
      isActive={isEventActive(id)}
      onclick={() => handleEventSelect(id)}
      class={isEventActive(id) ? 'bg-sidebar-accent text-sidebar-accent-foreground' : ''}
    >
      {#snippet child({ props })}
        <a href="/console/events/{id}" {...props}>
          <File />
          <span>{title}</span>
        </a>
      {/snippet}
    </Sidebar.MenuButton>
    <DropdownMenu.Root>
      <DropdownMenu.Trigger>
        {#snippet child({ props })}
          <Sidebar.MenuAction showOnHover {...props}>
            <Ellipsis />
            <span class="sr-only">More</span>
          </Sidebar.MenuAction>
        {/snippet}
      </DropdownMenu.Trigger>
      <DropdownMenu.Content
        class="w-48 rounded-lg"
        side={sidebar.isMobile ? "bottom" : "right"}
        align={sidebar.isMobile ? "end" : "start"}
      >
        <DropdownMenu.Item onclick={() => handleEventSelect(id)}>
          <Folder class="text-muted-foreground" />
          <span>查看事件</span>
        </DropdownMenu.Item>
        <DropdownMenu.Item>
          <Forward class="text-muted-foreground" />
          <span>分享事件</span>
        </DropdownMenu.Item>
        <DropdownMenu.Separator />
        <DropdownMenu.Item onclick={() => handleEventDelete(id)}>
          <Trash2 class="text-muted-foreground" />
          <span>删除事件</span>
        </DropdownMenu.Item>
      </DropdownMenu.Content>
    </DropdownMenu.Root>
  </Sidebar.MenuItem>
{/snippet}
