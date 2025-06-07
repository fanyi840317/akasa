<script lang="ts">
  import {
    Share2,
    MoreHorizontal,
    ChevronRight,
    ChevronLeft,
    Clock,
    Copy,
    QrCode,
    ImageIcon,
    Download,
    Trash2,
    Edit
  } from "lucide-svelte";
  import { Button } from "$lib/components/ui/button";
  import { Avatar, AvatarImage, AvatarFallback } from "$lib/components/ui/avatar";
  import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
    DropdownMenuSeparator
  } from "$lib/components/ui/dropdown-menu";
  import {
    Collapsible,
    CollapsibleContent,
    CollapsibleTrigger
  } from "$lib/components/ui/collapsible";
  import { Tooltip, TooltipContent, TooltipTrigger } from "$lib/components/ui/tooltip";
  // 使用简化的日期格式化，避免依赖问题
  function formatTimeAgo(date: Date): string {
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffSec = Math.floor(diffMs / 1000);
    const diffMin = Math.floor(diffSec / 60);
    const diffHour = Math.floor(diffMin / 60);
    const diffDay = Math.floor(diffHour / 24);
    const diffMonth = Math.floor(diffDay / 30);
    const diffYear = Math.floor(diffMonth / 12);

    if (diffYear > 0) return `${diffYear}年前`;
    if (diffMonth > 0) return `${diffMonth}个月前`;
    if (diffDay > 0) return `${diffDay}天前`;
    if (diffHour > 0) return `${diffHour}小时前`;
    if (diffMin > 0) return `${diffMin}分钟前`;
    return "刚刚";
  }

  // Props
  let {
    onEdit = () => {},
    onShare = () => {},
    onCopy = () => {},
    onTwitter = () => {},
    onFacebook = () => {},
    onQrCode = () => {},
    onCoverUpload = () => {},
    onExport = () => {},
    onDelete = () => {},
    onToggleSidebar = () => {},
    isSidebarOpen = $bindable(true),
    isShareOpen = $bindable(false),
    creator = $bindable({
      name: "未知用户",
      avatar: null
    }),
    lastModified = $bindable(new Date().toISOString()),
    createdAt = $bindable(new Date().toISOString())
  } = $props<{
    onEdit?: () => void;
    onShare?: () => void;
    onCopy?: () => void;
    onTwitter?: () => void;
    onFacebook?: () => void;
    onQrCode?: () => void;
    onCoverUpload?: () => void;
    onExport?: () => void;
    onDelete?: () => void;
    onToggleSidebar?: () => void;
    isSidebarOpen?: boolean;
    isShareOpen?: boolean;
    creator?: {
      name: string;
      avatar: string | null;
    };
    lastModified?: string;
    createdAt?: string;
  }>();

  // Format the dates
  let lastModifiedFormatted = $state("");
  $effect.pre(() => {
    lastModifiedFormatted = formatTimeAgo(new Date(lastModified));
  });

  // Handle sidebar toggle
  function handleToggleSidebar() {
    isSidebarOpen = !isSidebarOpen;
    if (typeof onToggleSidebar === 'function') {
      onToggleSidebar();
    }
  }

  // Get creator initials for avatar fallback
  function getInitials(name: string): string {
    return name
      .split(' ')
      .map((part: string) => part.charAt(0))
      .join('')
      .toUpperCase()
      .substring(0, 2);
  }
</script>

<div class="flex items-center gap-3">
  <!-- 编辑信息 -->
  <div class="flex items-center gap-2 text-xs text-muted-foreground mr-1">
    <Tooltip>
      <TooltipTrigger>
        <div class="flex items-center gap-1 cursor-help">
          <Clock class="h-3.5 w-3.5" />
          <span>编辑于 {lastModifiedFormatted}</span>
        </div>
      </TooltipTrigger>
      <TooltipContent side="bottom">
        <div class="text-xs">
          <div>创建于: {new Date(createdAt).toLocaleString('zh-CN')}</div>
          <div>最后编辑: {new Date(lastModified).toLocaleString('zh-CN')}</div>
        </div>
      </TooltipContent>
    </Tooltip>
  </div>

  <!-- 创建者信息 -->
  <div class="flex items-center gap-1.5">
    <Avatar class="h-6 w-6">
      {#if creator.avatar}
        <AvatarImage src={creator.avatar} alt={creator.name} />
      {/if}
      <AvatarFallback class="text-xs">{getInitials(creator.name)}</AvatarFallback>
    </Avatar>
    <span class="text-xs font-medium">{creator.name}</span>
  </div>

  <!-- 分享按钮组 -->
  <Collapsible bind:open={isShareOpen} class="relative">
    <CollapsibleTrigger>
      <Button variant="ghost" size="icon" class="h-8 w-8">
        <Share2 class="h-4 w-4" />
      </Button>
    </CollapsibleTrigger>
    <CollapsibleContent class="absolute right-0 top-full mt-1 z-50 bg-popover rounded-md shadow-md border border-border p-1">
      <div class="flex gap-1">
        <Button variant="ghost" size="icon" class="h-7 w-7" onclick={onCopy}>
          <Copy class="h-3.5 w-3.5" />
        </Button>
        <Button variant="ghost" size="icon" class="h-7 w-7" onclick={onTwitter}>
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 4s-.7 2.1-2 3.4c1.6 10-9.4 17.3-18 11.6 2.2.1 4.4-.6 6-2C3 15.5.5 9.6 3 5c2.2 2.6 5.6 4.1 9 4-.9-4.2 4-6.6 7-3.8 1.1 0 3-1.2 3-1.2z"></path></svg>
        </Button>
        <Button variant="ghost" size="icon" class="h-7 w-7" onclick={onFacebook}>
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path></svg>
        </Button>
        <Button variant="ghost" size="icon" class="h-7 w-7" onclick={onQrCode}>
          <QrCode class="h-3.5 w-3.5" />
        </Button>
      </div>
    </CollapsibleContent>
  </Collapsible>

  <!-- 编辑按钮 -->
  <Button variant="ghost" size="icon" class="h-8 w-8" onclick={onEdit}>
    <Edit class="h-4 w-4" />
  </Button>

  <!-- 更多操作 -->
  <DropdownMenu>
    <DropdownMenuTrigger>
      <Button variant="ghost" size="icon" class="h-8 w-8">
        <MoreHorizontal class="h-4 w-4" />
      </Button>
    </DropdownMenuTrigger>
    <DropdownMenuContent align="end">
      <DropdownMenuItem onclick={onCoverUpload}>
        <ImageIcon class="h-4 w-4 mr-2" />
        更换封面
      </DropdownMenuItem>
      <DropdownMenuItem onclick={onExport}>
        <Download class="h-4 w-4 mr-2" />
        导出
      </DropdownMenuItem>
      <DropdownMenuSeparator />
      <DropdownMenuItem onclick={onDelete} class="text-destructive focus:text-destructive">
        <Trash2 class="h-4 w-4 mr-2" />
        删除
      </DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>

  <!-- 侧边栏切换 -->
  <Tooltip>
    <TooltipTrigger>
      <Button variant="ghost" size="icon" class="h-8 w-8" onclick={handleToggleSidebar}>
        {#if isSidebarOpen}
          <ChevronRight class="h-4 w-4" />
        {:else}
          <ChevronLeft class="h-4 w-4" />
        {/if}
      </Button>
    </TooltipTrigger>
    <TooltipContent side="bottom">
      {isSidebarOpen ? '收起侧边栏' : '展开侧边栏'}
    </TooltipContent>
  </Tooltip>
</div>
