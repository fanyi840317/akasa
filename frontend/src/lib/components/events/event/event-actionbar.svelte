<script lang="ts">
  import {
    X,
    Save as SaveIcon,
    Pencil,
    Settings2,
    ArrowLeftIcon,
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
  import { Clock } from "lucide-svelte"; // Import Clock icon
  import CoverCard from "./actionbar-cards/cover-card.svelte";
  import DateCard from "./actionbar-cards/date-card.svelte";
  import MapCard from "./actionbar-cards/map-card.svelte";
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
</script>

<div class="relative w-full bg-base-200/10 border-b-[0.4px] border-base-content/10">
  <div
    class="flex gap-x-4 h-16 relative p-3 items-center w-full justify-between"
  >
    <div
      class="flex gap-8 text-sm min-w-[500px] justify-between  max-lg:w-full!"
      style="width: 643px;"
    >
      <div class="flex shrink items-center gap-2">
        <button class="btn btn-sm btn-ghost btn-neutral" onclick={onClose}>
          <ArrowLeftIcon class="w-4 h-4" />
          Events
        </button>
        <div
          class="relative shrink text-sm leading-snug flex grow flex-col w-full"
        >
          <div class="flex justify-between w-full">
            <h3 class="font-semibold flex gap-2">
              <span class="line-clamp-1 text-left">{title}</span>
            </h3>
          </div>
          <p class="font-normal line-clamp-1 text-neutral-content/50 text-xs">
            {summary || "没有描述"}
          </p>
        </div>
      </div>
    </div>
    <div class="absolute right-0 lg:pr-3 shrink-0 lg:block hidden">
      <div
        class="gap-2 h-0 items-center flex text-sm font-medium"
        style="z-index: 4;"
      >
        <div class="flex gap-2 select-none relative justify-start items-center">
          <UserAvatar
            class="size-6 group-hover:opacity-100 opacity-80 transition-opacity"
            fallback="F"
          ></UserAvatar>
        </div>
        <button
          class="btn rounded-full btn-neutral"
          onclick={() => {
            isCommentsPanelOpen = !isCommentsPanelOpen;
          }}>添加评论</button
        >
      </div>
    </div>
  </div>
</div>
