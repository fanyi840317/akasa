<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import { Input } from "$lib/components/ui/input";
  import { Check, Undo2, Pencil } from "lucide-svelte";
  import { fade } from "svelte/transition";
  import { createEventDispatcher } from "svelte";
    import { bind } from "leaflet";

  const dispatch = createEventDispatcher();

  let {
    value = $bindable(""),
    placeholder = "",
    class: className = "",
    disabled = false,
  } = $props<{
    value: string;
    placeholder?: string;
    class?: string;
    disabled?: boolean;
  }>();

  let isEditing = $state(false);
  let originalValue = $state("");
  let inputValue = $state(value);

  function startEditing() {
    if (disabled) return;
    originalValue = value;
    inputValue = value;
    isEditing = true;
  }

  function confirmEdit() {
    value = inputValue;
    isEditing = false;
    dispatch("change", { value: inputValue });
  }

  function cancelEdit() {
    inputValue = originalValue;
    isEditing = false;
  }

  $effect(() => {
    inputValue = value;
  });
</script>

<div class="flex items-center gap-2 w-full">
  {#if isEditing}
    <div class="flex items-center gap-2 w-full" in:fade={{ duration: 300 }}>
      <div class="relative flex-1">
        <Input
          {placeholder}
          class={`${className} pr-10`}
          bind:value={inputValue}
          {disabled}
        />
        {#if originalValue !== inputValue}
          <Button
            variant="ghost"
            size="icon"
            class="absolute right-0 top-0"
            onclick={cancelEdit}
            {disabled}
          >
            <Undo2 class="h-4 w-4" />
          </Button>
        {/if}
      </div>
      <Button
        variant="outline"
        size="icon"
        onclick={confirmEdit}
        {disabled}
      >
        <Check class="h-4 w-4" />
      </Button>
    </div>
  {:else}
    <div class="flex items-center gap-2 w-full" in:fade={{ duration: 300 }}>
      {#if value}
        <span class="flex-1">{value}</span>
      {:else}
        <span class="flex-1 text-muted-foreground/80">{placeholder}</span>
      {/if}
      <Button
        variant="ghost"
        size="icon"
        onclick={startEditing}
        {disabled}
      >
        <Pencil class="h-4 w-4" />
      </Button>
    </div>
  {/if}
</div>