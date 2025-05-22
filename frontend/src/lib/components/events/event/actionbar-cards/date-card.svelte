<script lang="ts">
  import ActionBarCard from "./actionbar-card.svelte";
  import { ChevronLeft, ChevronRight, Clock } from "lucide-svelte";
  import { formatDistanceToNow } from "date-fns";
  import { zhCN } from "date-fns/locale";
  import { cn } from "$lib/utils";
  import "cally";
  import {Card} from "$lib/components/ui/card"

  import { onMount } from "svelte";

  let {
    eventDate = $bindable(undefined),
    class: className = "",
    ...restProps
  } = $props<{
    eventDate?: string;
    class?: string;
  }>();

  let showCalendar = $state(false);
  let dateInput = $state(eventDate || "");

  onMount(async () => {
    // Attempt to load cally from CDN
    if (!customElements.get("calendar-date")) {
      try {
        // await import(/* @vite-ignore */ 'https://unpkg.com/cally');
        console.log("Cally loaded from CDN");
      } catch (e) {
        console.error("Failed to load Cally from CDN:", e);
      }
    }
  });

  function handleDateChange(e: CustomEvent) {
    // Add safety check for e.detail and e.detail.valueAsDate
    if (e.detail && e.detail.valueAsDate) {
      const newDate = e.detail.valueAsDate;
      // Format to YYYY-MM-DD to be consistent with potential string input
      const year = newDate.getFullYear();
      const month = (newDate.getMonth() + 1).toString().padStart(2, "0");
      const day = newDate.getDate().toString().padStart(2, "0");
      eventDate = `${year}-${month}-${day}`;
      dateInput = eventDate;
      showCalendar = false; // Hide calendar after selection
    }
  }

  function handleInputChange(e: Event) {
    const target = e.target as HTMLInputElement;
    dateInput = target.value;
    // Basic validation or allow any string as per requirement
    eventDate = dateInput;
  }

  function toggleCalendar() {
    showCalendar = !showCalendar;
  }

  let relativeTime = $derived("");
  let dateInputRef: HTMLInputElement;

  $effect(() => {
    if (showCalendar && dateInputRef) {
      dateInputRef.focus();
    }
  });

  $effect(() => {
    if (eventDate) {
      const date = new Date(eventDate);
      if (!isNaN(date.getTime())) {
        // Check if the date is valid
        try {
          relativeTime = formatDistanceToNow(date, {
            addSuffix: true,
            locale: zhCN,
          });
        } catch (e) {
          console.error("Error formatting date:", e);
          relativeTime = "日期格式无效"; // Fallback for formatting errors
        }
      } else {
        relativeTime = eventDate; // Display original string if date is invalid
      }
    } else {
      relativeTime = "发生时间";
    }
  });
</script>

<div class="dropdown dropdown-start">
  <!-- svelte-ignore a11y_no_noninteractive_tabindex -->
  <div class="tooltip tooltip-bottom tooltip-base-100" tabindex="0">
    <div class="tooltip-content p-2 px-4">
      <!-- Tooltip content for date, maybe show full date or something -->
      {#if eventDate}
        <span class="text-neutral-content/50 text-xs font-semibold"
          >{new Date(eventDate).toLocaleDateString()}</span
        >
      {:else}
        <span class="text-neutral-content/50 text-xs font-semibold"
          >暂无日期</span
        >
      {/if}
    </div>
    <ActionBarCard
      role="button"
      tabindex="0"
      class={cn("w-auto", className)}
      {...restProps}
    >
      <div class="flex items-center text-xs px-2 text-gray-500">
        <Clock class="w-3 h-3 mr-1" />
        <span class="font-semibold">{relativeTime}</span>
      </div>
    </ActionBarCard>
  </div>
  <!-- svelte-ignore a11y_no_noninteractive_tabindex -->
  <div
    tabindex="0"
    class="dropdown-content mt-2 "
  >
    <div class="relative gap-1 items-start">
      <Card
        class="flex-col justify-end items-end p-4 "
      >
        <fieldset
          class="fieldset w-[300px]"
        >
          <legend class="fieldset-legend">发生时间</legend>
          <input
            type="text"
            placeholder="输入日期 (YYYY-MM-DD)"
            class="editor-fix-input w-full"
            value={dateInput}
            oninput={handleInputChange}
            onfocus={() => (showCalendar = true)}
            bind:this={dateInputRef}
          />
          <p class="label">你也可以直接填写如:“公元xx年”</p>
        </fieldset>
        <button class="btn btn-sm btn-neutral mt-2">修改</button>
      </Card>
      {#if showCalendar}
        <Card class="absolute top-24 left-4 p-0">
          {#if customElements.get("calendar-date")}
            <calendar-date
              class="cally rounded-box border border-base-300 mt-1"
              onchange={handleDateChange}
              value={eventDate}
            >
              <button slot="previous" aria-label="Previous" class="p-1"
                ><ChevronLeft class="size-4" /></button
              >
              <button slot="next" aria-label="Next" class="p-1"
                ><ChevronRight class="size-4" /></button
              >
              <calendar-month></calendar-month>
            </calendar-date>
          {:else}
            <p class="text-xs text-warning">
              日期选择器加载失败。请检查网络连接或尝试刷新。
            </p>
          {/if}
        </Card>
      {/if}
    </div>
  </div>
</div>
