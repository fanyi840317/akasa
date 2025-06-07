<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import * as Popover from "$lib/components/ui/popover";
  import { MapPin } from "lucide-svelte";
  import { cn } from "$lib/utils";
  import MapPicker from "./map-picker.svelte";
  import type { LocationChangeEvent } from '.';

  export let value = "";
  export let placeholder = "选择位置";

  let showMapPicker = false;

  function handleLocationChange(event: CustomEvent<LocationChangeEvent>) {
    const { address, location } = event.detail;
    value = address;
  }
</script>

<div class="relative">
  <Popover.Root>
    <Popover.Trigger>
      <Button
        variant="outline"
        class={cn(
          "justify-start text-left font-normal w-full h-7 py-1 px-2",
          !value && "text-muted-foreground"
        )}
      >
        <MapPin class=" h-3 w-3" />
        {#if value}
          {value}
        {:else}
          {placeholder}
        {/if}
      </Button>
    </Popover.Trigger>
    <Popover.Content class="w-[400px] p-2" align="start">
      <MapPicker
        bind:value
        {placeholder}
        on:locationChange={handleLocationChange}
      />
    </Popover.Content>
  </Popover.Root>
</div>