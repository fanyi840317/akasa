<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import AffineEditor from "$lib/components/ui/editor/affine-editor.svelte";
  import { exportDoc } from "$lib/components/ui/editor/affine-editor";
  import { eventStore } from "$lib/stores/event";
  import { _ } from "svelte-i18n";
  import {
    Clock,
    MapPin,
    Sparkles,
    Eye,
    Share2,
    Image,
    Twitter,
    Facebook,
    QrCode,
    Copy,
  } from "lucide-svelte";
  import { Button } from "$lib/components/ui/button";
  import { Card } from "$lib/components/ui/card";
  import { Badge } from "$lib/components/ui/badge";
  import {
    Tabs,
    TabsContent,
    TabsList,
    TabsTrigger,
  } from "$lib/components/ui/tabs";
  import { type DateValue, getLocalTimeZone } from "@internationalized/date";
  import type { HtmlDoc } from "$lib/types/types";
  import type { Event } from "$lib/types/event";
  import { toast } from "svelte-sonner";
  import DatePicker from "$lib/components/ui/date-picker/date-picker.svelte";
  import MapPicker from "$lib/components/ui/map/map-picker.svelte";
  import type { LocationChangeEvent, LocationData } from "$lib/components/ui/map";
  import { fly } from "svelte/transition";
  import { onMount } from "svelte";
  import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
  } from "$lib/components/ui/dialog";
  import {
    Tooltip,
    TooltipContent,
    TooltipProvider,
    TooltipTrigger,
  } from "$lib/components/ui/tooltip";
  import { Switch } from "$lib/components/ui/switch";
  import { Label } from "$lib/components/ui/label";
  import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
  } from "$lib/components/ui/dropdown-menu";
  import { PUBLIC_MAPBOX_TOKEN } from "$env/static/public";
  import { getCurrentLocation } from "$lib/services/location";

  interface Props {
    x_event?: Omit<Event, "$id" | "$createdAt" | "$updatedAt"> & {
      is_public?: boolean;
    };
  }

  // 状态管理
  let { x_event }: Props = $props();
  let dateValue: DateValue | undefined = undefined;
  let isPublishing = $state(false);
  let newDoc: HtmlDoc = { content: x_event?.content || "" };
  let isTimeUnknown = $state(false);
  let startDate: DateValue | undefined = undefined;
  let endDate: DateValue | undefined = undefined;
  let timePreset = $state<"exact" | "preset" | "unknown">("exact");
  let isPublic = $state(false);
  let showPreview = $state(false);
  let previewContent = $state("");
  let showShareMenu = $state(false);
  let showQRCode = $state(false);
  let shareUrl = $state("");
  let coverImage = $state(x_event?.cover || "");
  let isUploading = $state(false);
  let isLocating = $state(false);
  let locationData:LocationData|undefined = $state();
  let shouldRequestLocation = $state(false);

  // 预设时间选项
  const timePresets = [
    { label: "很久以前", value: "ancient" },
    { label: "遥远的未来", value: "future" },
    { label: "某个夜晚", value: "night" },
    { label: "某个清晨", value: "morning" },
    { label: "某个黄昏", value: "dusk" },
    { label: "某个雨天", value: "rainy" },
  ];

  // 初始化默认事件对象
  if (!x_event) {
    x_event = {
      title: "",
      content: "",
      location: "",
      date: "",
      user_id: "",
      cover: "",
    };
  }
  // 添加动画状态
  let showContent = $state(false);

  onMount(async () => {
    showContent = true;

    // 如果没有初始位置，设置 shouldRequestLocation 为 true
    if (!x_event?.location) {
        shouldRequestLocation = true;
    }

    // 如果没有初始位置，尝试获取用户位置
    if (!x_event?.location) {
      isLocating = true;
      try {
        const result = await getCurrentLocation();
        if (x_event) {
          x_event.location = result.address;
          x_event.location_data = JSON.stringify(result.location);
          locationData = result.location;
        }
      } catch (error) {
        console.error("获取位置失败:", error);
        toast.error("获取位置失败，请手动选择位置");
      } finally {
        isLocating = false;
      }
    }
  });

  $effect(() => {
    if (locationData && x_event) {
      x_event.latitude = locationData.latitude;
      x_event.longitude = locationData.longitude;
    }
  });

  const dispatch = createEventDispatcher();

  // 事件处理函数
  function handleDateChange(
    event: CustomEvent<{ date: DateValue }>,
    type: "start" | "end",
  ) {
    const { date } = event.detail;
    if (type === "start") {
      startDate = date;
    } else {
      endDate = date;
    }

    if (x_event) {
      if (isTimeUnknown) {
        x_event.date = "未知";
      } else if (startDate && endDate) {
        x_event.date = `${startDate.toDate(getLocalTimeZone()).toISOString().split("T")[0]} 至 ${endDate.toDate(getLocalTimeZone()).toISOString().split("T")[0]}`;
      } else if (startDate) {
        x_event.date = startDate
          .toDate(getLocalTimeZone())
          .toISOString()
          .split("T")[0];
      }
    }
  }

  function toggleUnknownTime() {
    isTimeUnknown = !isTimeUnknown;
    if (isTimeUnknown) {
      startDate = undefined;
      endDate = undefined;
      if (x_event) {
        x_event.date = "未知";
      }
    }
  }

  async function getEditorContent() {
    if (!newDoc?.doc) return { content: "", title: undefined };
    const result = await exportDoc(newDoc.doc);
    return result || { content: "", title: undefined };
  }

  function handleTimePresetSelect(preset: string) {
    if (x_event) {
      x_event.date = preset;
    }
  }

  function handleTimeTabChange(value: string) {
    timePreset = value as "exact" | "preset" | "unknown";
    if (value === "unknown") {
      isTimeUnknown = true;
      startDate = undefined;
      endDate = undefined;
      if (x_event) {
        x_event.date = "未知";
      }
    } else {
      isTimeUnknown = false;
    }
  }

  async function handlePreview() {
    const { content } = await getEditorContent();
    previewContent = content;
    showPreview = true;
  }

  async function handleShare(type: "copy" | "twitter" | "facebook" | "wechat") {
    const url = window.location.href;
    shareUrl = url;

    switch (type) {
      case "copy":
        await navigator.clipboard.writeText(url);
        toast.success("链接已复制到剪贴板");
        break;
      case "twitter":
        window.open(
          `https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}&text=${encodeURIComponent(x_event?.title || "")}`,
        );
        break;
      case "facebook":
        window.open(
          `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`,
        );
        break;
      case "wechat":
        showQRCode = true;
        break;
    }
  }

  async function handlePublish() {
    if (!x_event) return;

    isPublishing = true;
    try {
      const { content, title } = await getEditorContent();
      if (!title || !content) {
        toast.error("标题和内容不能为空");
        return;
      }

      const eventData = {
        title,
        content,
        location: x_event.location || "",
        date: x_event.date || "",
        user_id: x_event.user_id,
        is_public: isPublic,
        cover: x_event.cover,
        location_data: x_event.location_data,
      };

      const result = await eventStore.createEvent(eventData);
      if (result) {
        toast.success("事件发布成功！");
        // 自动复制分享链接
        await handleShare("copy");
        dispatch("close", { result });
      }
    } catch (e: any) {
      console.error("发布事件失败:", e);
      toast.error("发布失败，请重试");
    } finally {
      isPublishing = false;
    }
  }

  async function handleCoverUpload(event: {
    currentTarget: EventTarget & HTMLInputElement;
  }) {
    const input = event.currentTarget;
    if (!input.files?.length) return;

    const file = input.files[0];
    if (!file.type.startsWith("image/")) {
      toast.error("请上传图片文件");
      return;
    }

    isUploading = true;
    try {
      // 这里添加你的图片上传逻辑
      // 例如：上传到你的服务器或云存储
      // const response = await uploadImage(file);
      // coverImage = response.url;

      // 临时使用本地预览
      const reader = new FileReader();
      reader.onload = (e) => {
        coverImage = e.target?.result as string;
        if (x_event) {
          x_event.cover = coverImage;
        }
      };
      reader.readAsDataURL(file);

      toast.success("封面图片上传成功");
    } catch (error) {
      console.error("上传失败:", error);
      toast.error("上传失败，请重试");
    } finally {
      isUploading = false;
    }
  }
</script>

{#if showContent}
  <div class="relative h-[calc(100vh-280px)]">
    <div class="relative h-full flex flex-col">
      <!-- 顶部标题区域 -->
      <div
        class="relative flex-none h-[160px]"
        in:fly={{ y: 20, duration: 500, delay: 200 }}
      >
        <!-- 封面图片背景 -->
        <div class="absolute inset-0 w-full">
          {#if coverImage}
            <img
              src={coverImage}
              alt="事件封面"
              class="w-full h-full object-cover"
            />
            <div
              class="absolute inset-0 bg-gradient-to-b from-neutral-900/80 via-neutral-900/40 to-neutral-900"
            />
          {:else}
            <div class="w-full h-full" />
          {/if}
        </div>

        <!-- 标题区域 -->
        <div class="relative h-full flex items-center mt-4">
          <div class="w-full px-16">
            <div class="max-w-4xl mx-auto">
              <div class="flex items-center gap-4">
                <div class="flex-1">
                  <input
                    id="title"
                    type="text"
                    placeholder="为你的神秘事件命名..."
                    bind:value={x_event.title}
                    class="event-title-input w-full bg-transparent text-4xl font-semibold border-0 outline-none shadow-none focus:ring-0 px-0 py-0 h-auto placeholder:text-muted-foreground/40"
                  />
                </div>
                <div
                  class="flex items-center gap-2 border-l border-border/40 pl-4"
                >
                  <TooltipProvider>
                    <Tooltip>
                      <TooltipTrigger>
                        <label class="cursor-pointer">
                          <input
                            type="file"
                            accept="image/*"
                            class="hidden"
                            on:change={handleCoverUpload}
                            disabled={isUploading}
                          />
                          <Button variant="ghost" size="icon" class="h-8 w-8">
                            <Image class="h-4 w-4" />
                          </Button>
                        </label>
                      </TooltipTrigger>
                      <TooltipContent>更换封面</TooltipContent>
                    </Tooltip>
                  </TooltipProvider>
                  <TooltipProvider>
                    <Tooltip>
                      <TooltipTrigger>
                        <Button
                          variant="ghost"
                          size="icon"
                          class="h-8 w-8"
                          onclick={handlePreview}
                        >
                          <Eye class="h-4 w-4" />
                        </Button>
                      </TooltipTrigger>
                      <TooltipContent>预览</TooltipContent>
                    </Tooltip>
                  </TooltipProvider>
                  <TooltipProvider>
                    <Tooltip>
                      <TooltipTrigger>
                        <DropdownMenu bind:open={showShareMenu}>
                          <DropdownMenuTrigger>
                            <Button variant="ghost" size="icon" class="h-8 w-8">
                              <Share2 class="h-4 w-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end" class="w-48">
                            <DropdownMenuItem
                              onclick={() => handleShare("copy")}
                            >
                              <Copy class="mr-2 h-4 w-4" />
                              复制链接
                            </DropdownMenuItem>
                            <DropdownMenuItem
                              onclick={() => handleShare("twitter")}
                            >
                              <Twitter class="mr-2 h-4 w-4" />
                              分享到 Twitter
                            </DropdownMenuItem>
                            <DropdownMenuItem
                              onclick={() => handleShare("facebook")}
                            >
                              <Facebook class="mr-2 h-4 w-4" />
                              分享到 Facebook
                            </DropdownMenuItem>
                            <DropdownMenuItem
                              onclick={() => handleShare("wechat")}
                            >
                              <QrCode class="mr-2 h-4 w-4" />
                              微信扫码分享
                            </DropdownMenuItem>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </TooltipTrigger>
                      <TooltipContent>分享</TooltipContent>
                    </Tooltip>
                  </TooltipProvider>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 主要内容区域 -->
      <div class="flex-1 flex min-h-0 px-10">
        <!-- 左侧编辑区域 -->
        <div
          class="flex-1 overflow-hidden"
          in:fly={{ x: -20, duration: 500, delay: 400 }}
        >
          <div class="h-full">
            <AffineEditor htmlDoc={newDoc} />
          </div>
        </div>

        <!-- 右侧信息面板 -->
        <div
          class="w-[320px] border-l border-border/40"
          in:fly={{ x: 20, duration: 500, delay: 600 }}
        >
          <div class="p-4 space-y-4">
            <!-- 时间选择 -->
            <Card
              class="p-4 hover:border-primary/20 transition-all hover:shadow-lg hover:shadow-primary/10"
            >
              <div class="flex items-center gap-2 mb-4">
                <Clock class="w-4 h-4 text-primary/70" />
                <h3 class="text-sm font-medium text-muted-foreground">时间</h3>
              </div>

              <Tabs
                value={timePreset}
                onValueChange={handleTimeTabChange}
                class="w-full"
              >
                <TabsList class="grid w-full grid-cols-3 mb-4 p-1">
                  <TabsTrigger
                    value="exact"
                    class="text-xs data-[state=active]:bg-primary/10 data-[state=active]:text-primary rounded-sm transition-all"
                  >
                    具体时间
                  </TabsTrigger>
                  <TabsTrigger
                    value="preset"
                    class="text-xs data-[state=active]:bg-primary/10 data-[state=active]:text-primary rounded-sm transition-all"
                  >
                    预设时间
                  </TabsTrigger>
                  <TabsTrigger
                    value="unknown"
                    class="text-xs data-[state=active]:bg-primary/10 data-[state=active]:text-primary rounded-sm transition-all"
                  >
                    时间未知
                  </TabsTrigger>
                </TabsList>

                <TabsContent value="exact" class="space-y-2">
                  <DatePicker
                    value={startDate}
                    placeholder="开始时间"
                    on:dateChange={(e) => handleDateChange(e, "start")}
                  />
                  <DatePicker
                    value={endDate}
                    placeholder="结束时间"
                    on:dateChange={(e) => handleDateChange(e, "end")}
                  />
                </TabsContent>

                <TabsContent value="preset" class="space-y-2">
                  <div class="grid grid-cols-2 gap-2">
                    {#each timePresets as preset}
                      <Badge
                        variant="outline"
                        class="cursor-pointer hover:bg-primary/10 hover:border-primary/30 hover:text-primary transition-all hover:scale-[1.02] active:scale-[0.98]"
                        onclick={() => handleTimePresetSelect(preset.label)}
                      >
                        {preset.label}
                      </Badge>
                    {/each}
                  </div>
                </TabsContent>

                <TabsContent value="unknown">
                  <div
                    class="text-sm text-muted-foreground italic p-3 rounded-md border border-neutral-800/50 hover:border-primary/20 transition-all"
                  >
                    这个神秘事件发生的时间暂时无法确定
                  </div>
                </TabsContent>
              </Tabs>
            </Card>

            <!-- 地点选择 -->
            <Card
              class="h-[200px] hover:border-primary/20 transition-all hover:shadow-lg hover:shadow-primary/10 relative overflow-hidden"
            >
              <MapPicker {locationData}
                placeholder="选择神秘事件发生的地点..."
                {isLocating}
                autoRequest={false}
                shouldRequest={shouldRequestLocation}
              />
            </Card>

            <!-- 发布按钮 -->
            <div class="sticky bottom-4">
              <Button
                onclick={handlePublish}
                disabled={isPublishing}
                class="w-full gap-2 bg-primary/90 hover:bg-primary text-primary-foreground h-10 shadow-lg shadow-primary/20 hover:shadow-primary/30 transition-all hover:scale-[1.02] active:scale-[0.98]"
              >
                <Sparkles class="h-4 w-4" />
                <span>{isPublishing ? "正在发布..." : "发布神秘事件"}</span>
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- 预览对话框 -->
  <Dialog bind:open={showPreview}>
    <DialogContent class="max-w-4xl">
      <DialogHeader>
        <DialogTitle>预览事件</DialogTitle>
      </DialogHeader>
      <div class="mt-4 prose dark:prose-invert max-w-none">
        {@html previewContent}
      </div>
    </DialogContent>
  </Dialog>

  <!-- 微信二维码对话框 -->
  <Dialog bind:open={showQRCode}>
    <DialogContent class="max-w-sm">
      <DialogHeader>
        <DialogTitle>微信扫码分享</DialogTitle>
      </DialogHeader>
      <div class="flex flex-col items-center space-y-4">
        <div class="w-48 h-48 p-2">
          <!-- 这里可以添加二维码生成逻辑 -->
          <div
            class="w-full h-full flex items-center justify-center text-muted-foreground"
          >
            二维码占位
          </div>
        </div>
        <div class="text-sm text-muted-foreground text-center">
          请使用微信扫描二维码分享
        </div>
      </div>
    </DialogContent>
  </Dialog>
{/if}
