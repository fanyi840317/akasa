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
    align = "end",
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
    align?: "start" | "end";
  }>();
</script>

<DropdownMenu.Root >
  <DropdownMenu.Trigger>
    <IconButton class={className}>
      <MoreHorizontal class="w-4 h-4" />
    </IconButton>
  </DropdownMenu.Trigger>
  <DropdownMenu.Content {align} class="w-48">
    {#if showSettings}
      <DropdownMenu.Group>
        <DropdownMenu.GroupHeading>属性设置</DropdownMenu.GroupHeading>
        <DropdownMenu.Item onclick={onSettings}>
          <Clock class="w-4 h-4 mr-1" />
          设置开始时间
        </DropdownMenu.Item>
        <DropdownMenu.Item onclick={onSettings}>
          <MapPin class="w-4 h-4 mr-1" />
          地点设置
        </DropdownMenu.Item>
        <DropdownMenu.Item onclick={onSettings}>
          <Tag class="w-4 h-4 mr-1" />
          类型设置
        </DropdownMenu.Item>
        <DropdownMenu.Item onclick={onSettings}>
          <Zap class="w-4 h-4 mr-1" />
          影响设置
        </DropdownMenu.Item>
        <DropdownMenu.Item onclick={onSettings}>
          <FileText class="w-4 h-4 mr-1" />
          事件描述
        </DropdownMenu.Item>
      </DropdownMenu.Group>
      <DropdownMenu.Separator />
    {/if}

    {#if showRename}
      <DropdownMenu.Item onclick={onRename}>
        <FileEdit class="w-4 h-4 mr-1" />
        重命名
      </DropdownMenu.Item>
    {/if}

    {#if showShare}
      <DropdownMenu.Item onclick={onShare}>
        <Share2 class="w-4 h-4 mr-1" />
        分享
      </DropdownMenu.Item>
    {/if}

    {#if showDelete}
      <DropdownMenu.Item class="text-error" onclick={onDelete}>
        <Trash2 class="w-4 h-4 mr-1" />
        删除
      </DropdownMenu.Item>
    {/if}
  </DropdownMenu.Content>
</DropdownMenu.Root>
