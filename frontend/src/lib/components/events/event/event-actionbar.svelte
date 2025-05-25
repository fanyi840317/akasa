<script lang="ts">
  import {
    X,
    Save as SaveIcon,
    Pencil,
    Settings2,
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

{#if editable}
  <div
    class="p-2 flex justify-between items-center  

    absolute top-0 left-0 right-0 z-10 "
  >
    <div class="flex flex-row items-center gap-4">
      <button class="btn btn-sm btn-circle btn-ghost btn-neutral" onclick={onClose}>
        <X class="w-4 h-4" />
      </button>
      <h1 class="text-xl font-semibold mr-2">{title}</h1>
      <!-- <DateCard eventDate={eventTime ? eventTime.toISOString() : undefined} />-->
      <!-- <MapCard locationData={location} />  -->
      
      <!-- <div class="dropdown dropdown-center">
        <button
          class="btn btn-sm"
          class:btn-active={isPropertiesPanelOpen}
          onclick={() => {
            isPropertiesPanelOpen = !isPropertiesPanelOpen;
          }}
        >
          <Settings2 class="w-4 h-4 mr-1" />
          属性
         
        </button>
        <div class="dropdown-content">
          <ul class="menu menu-md w-full rouded-xl">
            <EventPropertyCard categories={[]} />
          </ul>
        </div>
      </div> -->

      <div class="dropdown dropdown-start">
        <button
          aria-label="Change cover"
          tabindex="0"
          class="btn btn-sm btn-circle btn-ghost btn-neutral"
        >
          <More class="w-4 h-4" />
        </button>
        <ul
          tabindex="0"
          class="menu menu-mddropdown-content bg-base-300
          dropdown-content bg-base-200 text-base-content rounded-box
          rounded-xl z-1 w-48 border border-white/5 shadow-2xl outline-1 outline-black/5"
        >
          <li>
            <button 
              ><FileEdit class="w-4 h-4 mr-1" />重命名</button
            >
          </li>
          <li>
            <button 
              ><ImageIcon class="w-4 h-4 mr-1" />设置封面</button
            >
          </li>
          <li><a><Trash2 class="w-4 h-4 mr-1" />删除</a></li>
          <li><a><Info class="w-4 h-4 mr-1" />查看属性</a></li>
        </ul>
      </div>
    </div>

    <div class="flex items-center gap-2">
      {#if showSaveButton}
      <button class="btn btn-ghost btn-neutral btn-sm" onclick={onSaveDocument}>
        <SaveIcon class="w-4 h-4 mr-1" />
        保存
      </button>
      {/if}
      <button
        class="btn btn-ghost btn-neutral btn-sm px-1 pr-2"
        onclick={() => {
          isCommentsPanelOpen = !isCommentsPanelOpen;
        }}
      >
        <UserAvatar
          class="size-6 group-hover:opacity-100 opacity-80 transition-opacity"
        ></UserAvatar>

        +添加评论
      </button>
    </div>
  </div>
{/if}

