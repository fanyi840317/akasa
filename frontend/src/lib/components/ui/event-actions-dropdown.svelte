<script lang="ts">
  import {
    MoreHorizontal,
    FileEdit,
    Share2,
    Trash2,
    Settings2,
    Clock,
    MapPin,
    Tag,
    Zap,
    FileText,
  } from "lucide-svelte";
  import { IconButton } from "$lib/components/ui/buttons";
  import * as DropdownMenu from "$lib/components/ui/dropdown-menu";

  let {
    onRename = () => {},
    onShare = () => {},
    onDelete = () => {},
    onSettings = () => {},
    showSettings = true,
    showRename = true,
    showShare = true,
    showDelete = true,
    class: className = "",
  } = $props<{
    onRename?: () => void;
    onShare?: () => void;
    onDelete?: () => void;
    onSettings?: () => void;
    showSettings?: boolean;
    showRename?: boolean;
    showShare?: boolean;
    showDelete?: boolean;
    class?: string;
  }>();
</script>

<DropdownMenu.Root>
  <DropdownMenu.Trigger>
    <IconButton class={className}>
      <MoreHorizontal class="w-4 h-4" />
    </IconButton>
  </DropdownMenu.Trigger>
  <DropdownMenu.Content align="start" class="w-48">
    {#if showSettings}
      <DropdownMenu.Group>
        <DropdownMenu.GroupHeading>属性设置</DropdownMenu.GroupHeading>
        <DropdownMenu.Item onclick={onSettings}>
          <Clock class="w-4 h-4 mr-2" />
          时间设置
        </DropdownMenu.Item>
        <DropdownMenu.Item onclick={onSettings}>
          <MapPin class="w-4 h-4 mr-2" />
          地点设置
        </DropdownMenu.Item>
        <DropdownMenu.Item onclick={onSettings}>
          <Tag class="w-4 h-4 mr-2" />
          类型设置
        </DropdownMenu.Item>
        <DropdownMenu.Item onclick={onSettings}>
          <Zap class="w-4 h-4 mr-2" />
          影响设置
        </DropdownMenu.Item>
        <DropdownMenu.Item onclick={onSettings}>
          <FileText class="w-4 h-4 mr-2" />
          事件描述
        </DropdownMenu.Item>
      </DropdownMenu.Group>
    {/if}

    {#if showRename}
      <DropdownMenu.Separator />
      <DropdownMenu.Item onclick={onRename}>
        <FileEdit class="w-4 h-4 mr-2" />
        重命名
      </DropdownMenu.Item>
    {/if}

    {#if showShare}
      <DropdownMenu.Item onclick={onShare}>
        <Share2 class="w-4 h-4 mr-2" />
        分享
      </DropdownMenu.Item>
    {/if}

    {#if showDelete}
      <DropdownMenu.Item class="text-error" onclick={onDelete}>
        <Trash2 class="w-4 h-4 mr-2" />
        删除
      </DropdownMenu.Item>
    {/if}
  </DropdownMenu.Content>
</DropdownMenu.Root>
