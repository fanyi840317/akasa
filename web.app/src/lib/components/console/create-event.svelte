<script lang="ts">
  import { Separator } from "$lib/components/ui/separator";
  import {
    Avatar,
    AvatarFallback,
    AvatarImage,
  } from "$lib/components/ui/avatar";
  import { Badge } from "$lib/components/ui/badge";
  import { ScrollArea } from "$lib/components/ui/scroll-area";
  import { Input } from "$lib/components/ui/input";
  import { onMount, onDestroy, setContext } from "svelte";
  import { browser } from "$app/environment";
  import { writable } from "svelte/store";
  import { createEventDispatcher } from "svelte";
  import AffineEditor from "$lib/components/ui/editor/affine-editor.svelte";
  // import type { AppState } from "$lib/components/ui/editor/affine-editor";
  import {
    createDocByHtml,
    exportDoc,
  } from "$lib/components/ui/editor/affine-editor";
  import { eventStore } from "$lib/stores/event";
  import { auth } from "$lib/stores/auth";
  import { toast, Toaster } from "svelte-sonner";
  import { _ } from "svelte-i18n";
  import {
    User,
    MapPin,
    Clock,
    Calendar as CalendarIcon,
    ChevronsUpDown,
    Save,
    Send,
  } from "lucide-svelte";
  import { Button } from "$lib/components/ui/button";
  import * as Popover from "$lib/components/ui/popover";
  import * as Collapsible from "$lib/components/ui/collapsible";
  import { cn } from "$lib/utils";
  import {
    DateFormatter,
    type DateValue,
    getLocalTimeZone,
  } from "@internationalized/date";
  import { RangeCalendar } from "$lib/components/ui/range-calendar";
  import { Label } from "../ui/label";
  import { createEmptyDoc } from "@blocksuite/presets";
  import { HtmlTransformer, type Html } from "@blocksuite/blocks";
  import type { Doc } from "@blocksuite/store";
  import type { HtmlDoc } from "$lib/types/types";
  import type { Event } from "$lib/types/event";

  // 组件属性类型定义
  interface Props {
    x_event?: Event;
  }
  // 组件属性
  let { x_event }: Props = $props();

  if (!x_event) {
    x_event = {
      title: "",
      content: "",
      location: "",
      date: "",
      user_id: "",
    };
  }

  let dateValue: DateValue | undefined = undefined;

  // 日期格式化器
  const df = new DateFormatter("zh-CN", {
    dateStyle: "long",
  });
  let newDoc: HtmlDoc = $state({ content: x_event?.content });
  // let newDoc: Doc | undefined = undefined;
  onMount(async () => {
    // 自动聚焦到标题输入框
    // 延迟一点时间后让编辑器获得焦点
    // newDoc = await createDocByHtml("ceen");
  });

  // 处理日期变化
  function handleDateChange(date: DateValue) {
    dateValue = date;
    if (date) {
      const jsDate = date.toDate(getLocalTimeZone());
      // eventDate = jsDate.toISOString().split("T")[0]; // 转换为YYYY-MM-DD格式
    } else {
      // eventDate = "";
    }
  }

  // 发布事件到Appwrite
  let isPublishing = $state(false);
  let editorContent = "";

  // 获取编辑器内容的函数
  async function getEditorContent() {
    // 这里应该实现从AffineEditor获取内容的逻辑
    // 由于当前实现可能不支持直接获取，我们先使用空字符串
    // 确保doc存在后再导出
    if (!newDoc?.doc) return "";
    return await exportDoc(newDoc.doc);
  }

  // 创建事件分发器
  const dispatch = createEventDispatcher();

  async function publishToAppwrite() {
    console.log(getEditorContent());

    // 标题已通过Input组件双向绑定到x_event.title
    if (!x_event?.title) {
      toast.error($_("validation.title_required"));
      return;
    }

    isPublishing = true;
    try {
      // 获取当前用户信息
      const user = $auth.user;
      if (!user) {
        throw new Error("用户未登录");
      }
      const content = await getEditorContent();
      console.log(content);
      // 检查是否有内容
      if (!content) {
        toast.error($_("validation.content_required"));
        return;
      }
      // 准备事件数据
      x_event.content = content;
      x_event.user_id = user.$id;

      // 使用eventStore创建事件
      const result = await eventStore.createEvent(x_event);

      toast.success("事件已成功发布！");

      // 发布成功后，触发close事件通知父组件关闭对话框，并传递新创建的事件ID
      dispatch("close", { result: result });
    } catch (e: any) {
      console.error("发布事件失败:", e);
      toast.error(e.message || $_("event.publish_failed"));
    } finally {
      isPublishing = false;
    }
  }
</script>

<!-- 标题输入区域 - Notion风格 -->
<div class="px-24 py-6">
  <input
    id="title"
    type="text"
    placeholder="无标题"
    bind:value={x_event.title}
    class="notion-title-input text-4xl font-bold border-none shadow-none focus-visible:ring-0 px-0 py-0 h-auto placeholder:text-muted-foreground/40"
  />
</div>

<ScrollArea orientation="vertical" class="h-[calc(100vh-200px)]">
  <AffineEditor htmlDoc={newDoc} />
</ScrollArea>

<!-- 底部按钮区域 -->
<div class="absolute px-24 bottom-20 left-0">
  <!-- <Label for="btns" class="text-muted-foreground/50 text-xs">你可以</Label> -->
  <div id="btns">
    <Button
      variant="outline"
      class={cn(
        " text-left  font-normal h-7 px-2 py-1 bg-background/80 backdrop-blur-smp-4",
        !x_event?.location && "text-muted-foreground/70",
      )}
      size="sm"
    >
      <MapPin class="h-3 w-3" />
      {x_event?.location || "添加位置"}
    </Button>
    <Popover.Root>
      <Popover.Trigger>
        <Button
          variant="outline"
          class={cn(
            " justify-start text-left  font-normal h-7 px-2 py-1",
            !dateValue && "text-muted-foreground/70",
          )}
          size="sm"
        >
          <CalendarIcon class="h-3 w-3" />
          {dateValue
            ? df.format(dateValue.toDate(getLocalTimeZone()))
            : "选择发生日期"}
        </Button>
      </Popover.Trigger>
      <Popover.Content class="w-auto p-0" align="start">
        <RangeCalendar
          type="single"
          bind:value={dateValue}
          on:valueChange={(e) => handleDateChange(e.detail)}
        />
      </Popover.Content>
    </Popover.Root>
    <Button
      onclick={publishToAppwrite}
      disabled={isPublishing}
      variant="ghost"
      class="gap-2 bg-background/80 backdrop-blur-smp-4 h-7 px-2 py-1"
    >
      <Send class="h-4 w-4 " />
      {isPublishing ? "发布中..." : "发布"}
    </Button>
  </div>
</div>
