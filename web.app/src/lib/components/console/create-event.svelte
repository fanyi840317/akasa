<script lang="ts">
  import { ScrollArea } from "$lib/components/ui/scroll-area";
  import { createEventDispatcher } from "svelte";
  import AffineEditor from "$lib/components/ui/editor/affine-editor.svelte";
  import { exportDoc } from "$lib/components/ui/editor/affine-editor";
  import { eventStore } from "$lib/stores/event";
  import { auth } from "$lib/stores/auth";
  import { _ } from "svelte-i18n";
  import { get } from "svelte/store";
  import { Send } from "lucide-svelte";
  import { Button } from "$lib/components/ui/button";
  import {
    DateFormatter,
    type DateValue,
    getLocalTimeZone,
  } from "@internationalized/date";
  import type { HtmlDoc } from "$lib/types/types";
  import type { Event } from "$lib/types/event";
  import { toast } from "svelte-sonner";
  import DatePicker from "$lib/components/ui/date-picker/date-picker.svelte";
  import LocationPicker from "$lib/components/ui/map/location-picker.svelte";
  import type { LocationChangeEvent } from "$lib/components/ui/map";

  interface Props {
    x_event?: Omit<Event, "$id" | "$createdAt" | "$updatedAt">;
  }

  // 状态管理
  let { x_event }: Props = $props();
  let dateValue: DateValue | undefined = undefined;
  let isPublishing = $state(false);
  let newDoc: HtmlDoc = {};

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

  const dispatch = createEventDispatcher();

  // 事件处理函数
  function handleDateChange(event: CustomEvent<{ date: DateValue }>) {
    const { date } = event.detail;
    dateValue = date;
    if (x_event) {
      x_event.date = date
        ? date.toDate(getLocalTimeZone()).toISOString().split("T")[0]
        : "";
    }
  }

  function handleLocationChange(event: CustomEvent<LocationChangeEvent>) {
    const { location, address } = event.detail;
    if (x_event) {
      x_event.location = address;
      x_event.location_data = location;
    }
  }

  async function getEditorContent() {
    if (!newDoc?.doc) return { content: "", title: undefined };
    const result = await exportDoc(newDoc.doc);
    return result || { content: "", title: undefined };
  }

  async function publishToAppwrite() {
    if (!x_event) return;

    isPublishing = true;
    try {
      const { content, title } = await getEditorContent();
      x_event.title = title;
      x_event.content = content;
      const result = await eventStore.createEvent({
        ...x_event,
      });
      if (result) {
        dispatch("close", { result });
      }
    } catch (e: any) {
      console.error("发布事件失败:", e);
    } finally {
      isPublishing = false;
    }
  }
</script>

<!-- <div class="px-24 py-6">
  <input
    id="title"
    type="text"
    placeholder="无标题"
    bind:value={x_event.title}
    class="notion-title-input text-4xl font-bold border-none shadow-none focus-visible:ring-0 px-0 py-0 h-auto placeholder:text-muted-foreground/40"
  />
</div> -->

<ScrollArea orientation="vertical" class="h-[calc(100vh-280px)]">
  <div id="btns" class="flex flex-wrap px-24 gap-2 mt-10 z-20 max-w-[800px]">
    <LocationPicker
      value={x_event?.location || ""}
      placeholder="添加位置"
      on:locationChange={handleLocationChange}
    />
    <DatePicker
      value={dateValue}
      placeholder="选择发生日期"
      on:dateChange={handleDateChange}
    />
  </div>
  <AffineEditor htmlDoc={newDoc} />
</ScrollArea>

<div class="absolute px-24 bottom-20 left-0">
  <div id="btns" class="flex flex-wrap gap-2">

    <Button
      onclick={publishToAppwrite}
      disabled={isPublishing}
      variant="ghost"
      class="gap-2 ml-4 bg-background/40 backdrop-blur-smp-4 h-7 px-2 py-1"
    >
      <Send class="h-4 w-4" />
      {isPublishing ? "发布中..." : "发布"}
    </Button>
  </div>
</div>
