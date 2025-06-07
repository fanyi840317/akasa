<script lang="ts">
  import {
    X,
    Save as SaveIcon,
    Pencil,
    Settings2,
    ArrowLeftIcon,
    LockIcon,
    Check,
    MoreHorizontalIcon as More,
    FileEdit, // For Rename
    ImageIcon, // For Set Cover
    Trash2, // For Delete
    Info, //
  } from "lucide-svelte";
  import CoverSelector from "./cover-selector.svelte";
  import { UserAvatar } from "$lib/components/ui/avatar";
  import { base } from "$app/paths";
  import * as Modal from "$lib/components/ui/modal";
  import { MoreIcon } from "@blocksuite/blocks";
  import EventPropertyCard from "./event-property-card.svelte";
  import MapBase from "$lib/components/map/map-base.svelte";
  import type { Location } from "$lib/types/map";
  import { Clock, Share2 } from "lucide-svelte"; // Import Clock and Share2 icons
  import CoverCard from "./actionbar-cards/cover-card.svelte";
  import DateCard from "./actionbar-cards/date-card.svelte";
  import MapCard from "./actionbar-cards/map-card.svelte";
  import { IconButton, OutlineButton } from "$lib/components/ui/buttons";
  import EventActionsDropdown from "$lib/components/ui/event-actions-dropdown.svelte";
  // import  from "daisyui/src/colors/themes";

  let {
    title = $bindable("Untitled Event"),
    showSaveButton = true,
    editable = true,
    onClose = () => {},
    onSaveDocument = () => {},
    onTitleChange = (newTitle: string) => {},
    isPropertiesPanelOpen = $bindable(false),
    isCommentsPanelOpen = $bindable(false),
    summary = $bindable(""),
    location = $bindable<Location | undefined>(undefined),
    onLocationChange = (newLocation: Location | undefined) => {},
    eventTime = $bindable<Date | null>(undefined), // New prop for event time
    onEventTimeChange = (newTime: Date | undefined) => {}, // New callback prop for time changes
    // onCoverChange?: (url: string) => void, // Example prop for handling cover changes
    userId, // 声明 userId 属性类型
    onShare = () => {}, // 添加分享事件处理函数
  } = $props<{
    // Added a placeholder for onCoverChange if needed later
    title?: string;
    showSaveButton?: boolean;
    editable?: boolean;
    onClose?: () => void;
    onSaveDocument?: () => void;
    onTitleChange?: (newTitle: string) => void;
    isPropertiesPanelOpen?: boolean;
    isCommentsPanelOpen?: boolean;
    summary?: string;
    location?: Location | null;
    onLocationChange?: (newLocation: Location | null) => void;
    eventTime?: Date | null; // New prop type
    onEventTimeChange?: (newTime: Date | null) => void; // New callback prop type
    userId?: string; // 声明 userId 属性类型
    onShare?: () => void; // 添加分享事件处理函数类型
  }>();

  let isCoverSelectorOpen = $state(false);
  let isRenaming = $state(false);
  let newTitle = $state(title);
  let currentCoverUrl = $state<string | undefined>(undefined); // To store the cover image URL
  let isEditingLocation = $state(false);
  let currentLocation = $state<Location | null>(location); // To store location coordinates
  let newLocation = $state<Location | null>(null);
  let isEditingTime = $state(false); // New state for time modal
  let newEventTime = $state<Date | null>(eventTime); // New state for selected time

  function handleShare() {
    // 调用父组件传入的分享处理函数
    console.log("分享按钮被点击");
    onShare();
  }
</script>

<div class="flex gap-x-4 relative p-3 items-center w-full justify-between">
  <div class="flex  items-center gap-2">
    <button class="btn btn-sm btn-ghost btn-neutral" onclick={onClose}>
      <ArrowLeftIcon class="w-4 h-4" />
      Events
    </button>
    <h3 class="font-semibold flex gap-2 items-center">
      {#if isRenaming}
        <div class="flex items-center gap-2">
          <input
            type="text"
            class="input input-sm input-bordered w-full max-w-xs"
            bind:value={newTitle}
            autofocus
            onkeydown={(e) => {
              if (e.key === "Enter") {
                if (newTitle.trim()) {
                  onTitleChange(newTitle);
                  isRenaming = false;
                }
              } else if (e.key === "Escape") {
                newTitle = title;
                isRenaming = false;
              }
            }}
          />
          <button
            class="btn btn-sm btn-ghost btn-circle"
            onclick={() => {
              if (newTitle.trim()) {
                onTitleChange(newTitle);
                isRenaming = false;
              }
            }}
          >
            <Check class="w-4 h-4" />
          </button>
          <button
            class="btn btn-sm btn-ghost btn-circle"
            onclick={() => {
              newTitle = title;
              isRenaming = false;
            }}
          >
            <X class="w-4 h-4" />
          </button>
        </div>
      {:else}
        <span class="line-clamp-1 text-left">{title}</span>
      {/if}
    </h3>
    <button class="btn btn-xs btn-ghost  border-border ">
      <LockIcon class="size-3 " />
      private
    </button>
  </div>
  <div
      class="gap-2 h-0 items-center flex text-sm font-medium"
      style="z-index: 4;"
    >
      <IconButton onclick={handleShare}>
        <Share2 class="w-4 h-4" />
      </IconButton>
      <EventActionsDropdown
        onSettings={() => (isPropertiesPanelOpen = !isPropertiesPanelOpen)}
        onRename={() => {
          isRenaming = true;
          newTitle = title;
        }}
        onShare={handleShare}
        onDelete={() => {
          // TODO: 实现删除逻辑
          console.log("删除事件");
        }}
      />
      <div class="flex gap-2 select-none relative justify-start items-center">
        <UserAvatar
          class="size-6 group-hover:opacity-100 opacity-80 transition-opacity"
          fallback="F"
        ></UserAvatar>
      </div>
      <button
        class="btn rounded-full btn-neutral btn-sm"
        onclick={() => {
          isCommentsPanelOpen = !isCommentsPanelOpen;
        }}>添加评论</button
      >
    </div>
</div>
