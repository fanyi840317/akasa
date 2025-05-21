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
  // import  from "daisyui/src/colors/themes";

  let {
    title = $bindable("Untitled Event"),
    showSaveButton = true,
    editableTitle = true,
    onClose = () => {},
    onSaveDocument = () => {},
    onTitleChange = (newTitle: string) => {},
    isPropertiesPanelOpen = $bindable(false),
    isCommentsPanelOpen = $bindable(false),
    summary = $bindable(""),
    location = $bindable<Location | null>(null),
    onLocationChange = (newLocation: Location | null) => {},
    eventTime = $bindable<Date | null>(null), // New prop for event time
    onEventTimeChange = (newTime: Date | null) => {}, // New callback prop for time changes
    // onCoverChange?: (url: string) => void, // Example prop for handling cover changes
  } = $props<{
    // Added a placeholder for onCoverChange if needed later
    title?: string;
    showSaveButton?: boolean;
    editableTitle?: boolean;
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
  }>();

  let isCoverSelectorOpen = $state(false);
  let isRenaming = $state(false);
  let newTitle = $state(title);
  let currentCoverUrl = $state<string | null>(null); // To store the cover image URL
  let isEditingLocation = $state(false);
  let currentLocation = $state<Location | null>(location); // To store location coordinates
  let newLocation = $state<Location | null>(null);
  let isEditingTime = $state(false); // New state for time modal
  let newEventTime = $state<Date | null>(eventTime); // New state for selected time

  $effect(() => {
    currentLocation = location;
  });

  $effect(() => {
    newEventTime = eventTime;
  });

  function toggleCoverSelector() {
    // if (!editableTitle) return; // Using editableTitle to gate cover changes for now
    isCoverSelectorOpen = !isCoverSelectorOpen;
  }

  // Event handlers for CoverSelector
  function handleCoverSelect(event: CustomEvent<{ url: string }>) {
    console.log("Cover selected in actionbar:", event.detail.url);
    currentCoverUrl = event.detail.url;
    // TODO: Dispatch an event or call a prop function to update the actual cover in the parent or data store
    // For example: $dispatch('coverChange', { url: event.detail.url });
    isCoverSelectorOpen = false;
  }

  function handleCoverUpload(event: CustomEvent<{ url: string }>) {
    // Assuming upload returns a URL
    console.log("Upload action triggered in actionbar, URL:", event.detail.url);
    currentCoverUrl = event.detail.url;
    // TODO: Implement actual upload logic and get URL from response
    isCoverSelectorOpen = false;
  }

  function handleCoverLinkSubmit(event: CustomEvent<{ url: string }>) {
    console.log("Link submitted in actionbar:", event.detail.url);
    currentCoverUrl = event.detail.url;
    // TODO: Dispatch an event or call a prop function to update the actual cover in the parent or data store
    isCoverSelectorOpen = false;
  }

  function handleSaveDocument() {
    onSaveDocument();
  }

  function startRename() {
    newTitle = title; // Initialize with current title
    isRenaming = true;
  }

  function confirmRename() {
    onTitleChange(newTitle);
    isRenaming = false;
  }

  function cancelRename() {
    isRenaming = false;
  }

  function startEditingLocation() {
    newLocation = currentLocation ? { ...currentLocation } : null;
    isEditingLocation = true;
  }

  function confirmLocationChange() {
    if (newLocation) {
      currentLocation = newLocation;
      onLocationChange(currentLocation);
      console.log("Location confirmed:", currentLocation);
    }
    isEditingLocation = false;
  }

  function cancelLocationChange() {
    isEditingLocation = false;
  }

  function handleMapClick(event: CustomEvent<{ lngLat: { lng: number; lat: number } }>) {
    newLocation = { coordinates: event.detail.lngLat };
    console.log("Map clicked, new location tentative:", newLocation);
  }
</script>

<div
  class="p-4 flex justify-between items-center absolute top-0 left-0 right-0 z-10"
>
  <div class="flex flex-row items-center gap-4">
    <button class="btn btn-sm btn-circle btn-ghost" onclick={onClose}>
      <X class="w-4 h-4" />
    </button>
    {#if editableTitle}
      <div
        class="flex flex-row  gap-2 "
      >
        {#if currentCoverUrl}
          <img
            src={currentCoverUrl}
            alt="Event Cover"
            class="rounded-lg object-cover border border-white/5 
            grayscale transition-all duration-500 group-hover:grayscale-0
            shadow-2xl outline-1 outline-black/5"
            style="width: 60px; height: 33px;"
          />
        {:else}
          <div
            class="rounded-lg flex items-center justify-center overflow-hidden
          bg-base-300 border border-white/5 shadow-2xl outline-1 outline-black/5"
            style="width: 60px; height: 33px;"
          >
            <span
              class="transform -rotate-5 text-[10px] font-semibold text-gray-500 dark:text-gray-400"
            >
              no cover
            </span>
          </div>
        {/if}
        <h1 class="text-xl font-semibold mr-2">{title}</h1>
      </div>
      <div
        class="flex flex-row text-base-content/70 hover:text-base-content
        text-[0.625rem] gap-2"
      >
        <button class="flex flex-row items-center gap-2 text-left" onclick={startEditingLocation}>
          <div
            class="rounded-lg flex items-center justify-center overflow-hidden
            bg-base-300 border border-white/5 shadow-2xl outline-1 outline-black/5"
            style="width: 60px; height: 33px;"
          >
            <MapBase bind:locationData={currentLocation} showUserLocation={false} clickable={false}></MapBase>
          </div>
          <div class="flex flex-col gap-0">
            <span class="font-semibold text-base-content">发生地点</span>
            {currentLocation?.coordinates ? `${currentLocation.coordinates.lng.toFixed(2)}, ${currentLocation.coordinates.lat.toFixed(2)}` : '未设置地点'}
          </div>
        </button>
        <!-- <button class="flex flex-row items-center gap-2 text-left" onclick={() => isEditingTime = true}>
          <div
            class="rounded-lg flex items-center justify-center overflow-hidden
            bg-base-300 border border-white/5 shadow-2xl outline-1 outline-black/5"
            style="width: 60px; height: 33px;"
          >
            <Clock class="w-4 h-4 text-gray-500 dark:text-gray-400" />
          </div>
          <div class="flex flex-col gap-0">
            <span class="font-semibold text-base-content">发生时间</span>
            {newEventTime ? newEventTime.toLocaleString() : '未设置时间'}
          </div>
        </button> -->
      </div>
      <button class="btn btn-sm bg-base-100 cursor-copy rounded-full font-mono font-light"
        ><Clock class="w-4 h-4 " />2002-2-2</button
      >
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
          class="btn btn-sm btn-circle btn-ghost"
        >
          <More class="w-4 h-4" />
        </button>
        <ul
          class="menu menu-mddropdown-content bg-base-300
          dropdown-content bg-base-200 text-base-content rounded-box
          rounded-xl z-1 w-48 border border-white/5 shadow-2xl outline-1 outline-black/5"
        >
          <li>
            <button onclick={startRename}
              ><FileEdit class="w-4 h-4 mr-1" />重命名</button
            >
          </li>
          <li>
            <button onclick={toggleCoverSelector}
              ><ImageIcon class="w-4 h-4 mr-1" />设置封面</button
            >
          </li>
          <li><a><Trash2 class="w-4 h-4 mr-1" />删除</a></li>
          <li><a><Info class="w-4 h-4 mr-1" />查看属性</a></li>
        </ul>
      </div>
    {/if}
  </div>

  <div class="flex items-center gap-2">
    {#if showSaveButton}
      <button class="btn btn-sm" onclick={handleSaveDocument}>
        <SaveIcon class="w-4 h-4 mr-1" />
        保存
      </button>
    {:else}
      <!-- Placeholder for alignment if save button is hidden -->
      <div
        class="w-[calc(theme(spacing.btn-sm)+theme(spacing.4)+theme(spacing.1))]"
      ></div>
      <!-- Adjusted width to match button + icon + margin -->
    {/if}
    <button
      class="btn btn-sm px-1 pr-2 bg-base-300"
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
<Modal.Root bind:open={isRenaming} class="w-[500px]">
  <div class="p-6 flex flex-col gap-4">
    <div class="font-semibold">重命名事件</div>
    <input
      type="text"
      class="editor-fix-input"
      bind:value={newTitle}
      placeholder="输入新的事件标题"
    />
  </div>
  <Modal.Foot onCancel={cancelRename} onConfirm={confirmRename}></Modal.Foot>
</Modal.Root>
<Modal.Root class="w-auto" bind:open={isCoverSelectorOpen}>
  <div class="p-6 flex flex-col gap-4">
    <div class="text-sm font-semibold">封面图片</div>
    <CoverSelector
      on:select={handleCoverSelect}
      on:upload={handleCoverUpload}
      on:linkSubmit={handleCoverLinkSubmit}
    />
  </div>
</Modal.Root>

<Modal.Root bind:open={isEditingTime} class="w-[400px]">
  <div class="p-6 flex flex-col gap-4">
    <div class="font-semibold">设置时间</div>
    <!-- TODO: Integrate a time/date picker component here -->
    <input type="datetime-local" bind:value={newEventTime} class="editor-fix-input" />
  </div>
  <Modal.Foot onCancel={() => isEditingTime = false} onConfirm={() => { onEventTimeChange(newEventTime); isEditingTime = false; }}></Modal.Foot>
</Modal.Root>

<Modal.Root bind:open={isEditingLocation} class="w-[600px] h-[500px]">
  <div class="p-6 flex flex-col gap-4 h-full">
    <div class="font-semibold">选择地点</div>
    <div class="flex-grow h-[calc(100%-100px)]"> <MapBase bind:locationData={currentLocation} onClick={handleMapClick} showGeocoder={true} clickable={true}></MapBase></div>
  </div>
  <Modal.Foot onCancel={cancelLocationChange} onConfirm={confirmLocationChange}></Modal.Foot>
</Modal.Root>
