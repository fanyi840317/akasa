<script lang="ts">
  import * as Breadcrumb from "$lib/components/ui/breadcrumb";
  import { Separator } from "$lib/components/ui/separator";
  import * as Sidebar from "$lib/components/ui/sidebar";

  let { items = [] } = $props<{
    items: { name: string; path: string; }[];
  }>();
</script>

<Sidebar.Trigger class="-ml-1" />
<Separator orientation="vertical" class="mr-2 h-4" />
<Breadcrumb.Root>
  <Breadcrumb.List>
    {#each items as item, index}
      <Breadcrumb.Item>
        <a href={item.path}>{item.name}</a>
      </Breadcrumb.Item>
      {#if index < items.length - 1}
        <Breadcrumb.Separator />
      {/if}
    {/each}
  </Breadcrumb.List>
</Breadcrumb.Root>