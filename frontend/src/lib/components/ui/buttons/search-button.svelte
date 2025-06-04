<script lang="ts">
  import { Search } from 'lucide-svelte';
  import { cn } from '$lib/utils';

  let {
    onClick = undefined,
    class: className = '',
    size = 'default',
    variant = 'default',
    showShortcut = true,
    shortcutKeys = ['Ctrl', 'K'],
    disabled = false,
    ...restProps
  } = $props<{
    onClick?: () => void;
    class?: string;
    size?: 'sm' | 'default' | 'lg';
    variant?: 'default' | 'ghost' | 'outline';
    showShortcut?: boolean;
    shortcutKeys?: string[];
    disabled?: boolean;
    [key: string]: any;
  }>();

  const sizeClasses = {
    sm: 'p-1.5 text-xs gap-1.5',
    default: 'p-2 text-xs gap-2',
    lg: 'p-3 text-sm gap-3'
  };

  const variantClasses = {
    default: 'bg-base-200/50 hover:bg-base-200 border border-base-300',
    ghost: 'hover:bg-base-200/50',
    outline: 'border border-base-content/50 hover:bg-base-200/30'
  };

  const iconSizes = {
    sm: 'w-3 h-3',
    default: 'w-4 h-4',
    lg: 'w-5 h-5'
  };
</script>

<button
  class={cn(
    'text-base-content/70 hover:text-base-content rounded-lg',
    'font-medium transition-all duration-200 cursor-pointer',
    'hover:scale-[1.02] hover:shadow-md',
    'flex items-center justify-center group',
    'disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100',
    sizeClasses[size],
    variantClasses[variant],
    className
  )}
  on:click={onClick}
  {disabled}
  {...restProps}
>
  <Search
    class={cn(
      'group-hover:scale-110 transition-transform duration-200',
      iconSizes[size]
    )}
  />
  Search
  
  {#if showShortcut && shortcutKeys.length > 0}
    <span class="ml-auto flex items-center gap-1">
      {#each shortcutKeys as key}
        <span class="text-xs opacity-50 kbd kbd-xs">{key}</span>
      {/each}
    </span>
  {/if}
</button>