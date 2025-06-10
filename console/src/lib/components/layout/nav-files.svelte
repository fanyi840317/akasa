<script lang="ts">
  import { ChevronRightIcon, FolderIcon, FileIcon } from '@lucide/svelte';
  import * as Collapsible from "$lib/components/ui/collapsible/index.js";
  import * as Sidebar from "$lib/components/ui/sidebar/index.js";
  import type { Component, ComponentProps } from "svelte";
  let { files }: { files: [] } =
		$props();

</script>


<Sidebar.Menu>
    {#each files as item, index (index)}
      {@render Tree({ item })}
    {/each}
  </Sidebar.Menu>

  {#snippet Tree({ item }: { item: string | any[] })}
  {@const [name, ...items] = Array.isArray(item) ? item : [item]}
  {#if !items.length}
    <Sidebar.MenuButton
      isActive={name === "button.svelte"}
      class="data-[active=true]:bg-transparent"
    >
      <FileIcon />
      {name}
    </Sidebar.MenuButton>
  {:else}
    <Sidebar.MenuItem>
      <Collapsible.Root
        class="group/collapsible [&[data-state=open]>button>svg:first-child]:rotate-90"
        open={name === "lib" || name === "components"}
      >
        <Collapsible.Trigger>
          {#snippet child({ props })}
            <Sidebar.MenuButton {...props}>
              <ChevronRightIcon className="transition-transform" />
              <FolderIcon />
              {name}
            </Sidebar.MenuButton>
          {/snippet}
        </Collapsible.Trigger>
        <Collapsible.Content>
          <Sidebar.MenuSub>
            {#each items as subItem, index (index)}
              {@render Tree({ item: subItem })}
            {/each}
          </Sidebar.MenuSub>
        </Collapsible.Content>
      </Collapsible.Root>
    </Sidebar.MenuItem>
  {/if}
{/snippet}