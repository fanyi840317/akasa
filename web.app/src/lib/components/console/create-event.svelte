<script lang="ts">
  import { ScrollArea } from "$lib/components/ui/scroll-area";
  import { createEventDispatcher } from "svelte";
  import AffineEditor from "$lib/components/ui/editor/affine-editor.svelte";
  import { exportDoc } from "$lib/components/ui/editor/affine-editor";
  import { eventStore } from "$lib/stores/event";
  import { auth } from "$lib/stores/auth";
  import { _ } from "svelte-i18n";
  import { MapPin, Calendar as CalendarIcon, Send } from "lucide-svelte";
  import { Button } from "$lib/components/ui/button";
  import * as Popover from "$lib/components/ui/popover";
  import { cn } from "$lib/utils";
  import {
    DateFormatter,
    type DateValue,
    getLocalTimeZone,
  } from "@internationalized/date";
  import { Calendar } from "$lib/components/ui/calendar";
  import type { HtmlDoc } from "$lib/types/types";
  import type { Event } from "$lib/types/event";
  import { toast } from "svelte-sonner";
  import DatePicker from "$lib/components/ui/date-picker/date-picker.svelte";
  import LocationPicker from "$lib/components/ui/map/location-picker.svelte";

  interface Props {
    x_event?: Event;
  }

  // 状态管理
  let { x_event }: Props = $props();
  let dateValue: DateValue | undefined = undefined;
  let isPublishing = $state(false);
  let newDoc: HtmlDoc = $state({ content: x_event?.content });

  // 初始化默认事件对象
  if (!x_event) {
    x_event = {
      title: "",
      content: "",
      location: "",
      date: "",
      user_id: "",
    };
  }

  // 工具函数
  const df = new DateFormatter("zh-CN", {
    dateStyle: "long",
  });

  const dispatch = createEventDispatcher();

  // 事件处理函数
  function handleDateChange(event: CustomEvent<{date: DateValue}>) {
    const { date } = event.detail;
    dateValue = date;
    if (x_event)
      x_event.date = date
        ? date.toDate(getLocalTimeZone()).toISOString().split("T")[0]
        : "";
  }

  function handleLocationChange(event: CustomEvent<{location: string}>) {
    const { location } = event.detail;
    if (x_event) {
      x_event.location = location;
    }
  }

  async function getEditorContent() {
    if (!newDoc?.doc) return "";
    return await exportDoc(newDoc.doc);
  }

  async function validateEvent() {
    if (!x_event?.title) {
      toast.error($_("validation.title_required"));
      return false;
    }

    const user = $auth.user;
    if (!user) {
      toast.error($_("validation.user_not_logged_in"));
      return false;
    }

    const content = await getEditorContent();
    if (!content) {
      toast.error($_("validation.content_required"));
      return false;
    }

    x_event.content = content;
    x_event.user_id = user.$id;
    return true;
  }

  async function publishToAppwrite() {
    if (!(await validateEvent())) return;

    isPublishing = true;
    try {
      const result = await eventStore.createEvent(x_event as Omit<Event, '$id'>);
      dispatch("close", { result });
    } catch (e: any) {
      console.error("发布事件失败:", e);
    } finally {
      isPublishing = false;
    }
  }
</script>

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

<div class="absolute px-24 bottom-20 left-0">
  <div id="btns" class="flex gap-2">
    <div class="w-[200px]">
      <LocationPicker
        value={x_event?.location || ""}
        placeholder="添加位置"
        on:locationChange={handleLocationChange}
      />
    </div>

    <div class="w-[200px]">
      <DatePicker
        value={dateValue}
        placeholder="选择发生日期"
        on:dateChange={handleDateChange}
      />
    </div>

    <Button
      onclick={publishToAppwrite}
      disabled={isPublishing}
      variant="ghost"
      class="gap-2 bg-background/80 backdrop-blur-smp-4 h-7 px-2 py-1"
    >
      <Send class="h-4 w-4" />
      {isPublishing ? "发布中..." : "发布"}
    </Button>
  </div>
</div>
