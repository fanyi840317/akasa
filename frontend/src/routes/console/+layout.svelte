<script lang="ts">
  import { Users, BarChart2, Shield, MessageSquare, Info, Settings, Search, ListFilter, FileText, ThumbsUp, ThumbsDown, MessageCircle, FileSearch } from 'lucide-svelte';
  import { page } from '$app/stores';
  import { auth } from '$lib/stores/auth'; // 假设 auth store 的路径
    import { UserAvatar } from '$lib/components/ui/avatar';
  import { BatchAddEvents } from '$lib/components/events';

  const categories = [
    { name: 'Discussion', icon: MessageSquare, color: 'bg-blue-500', path: '/console/categories/discussion' },
    { name: 'How To', icon: FileText, color: 'bg-orange-500', path: '/console/categories/how-to' }, // Assuming FileText is for 'How To'
    { name: 'Feature Requests', icon: ThumbsUp, color: 'bg-green-500', path: '/console/categories/feature-requests' }, // Assuming ThumbsUp is for 'Feature Requests'
    { name: 'Bug Reports', icon: ThumbsDown, color: 'bg-purple-500', path: '/console/categories/bug-reports' }, // Assuming ThumbsDown is for 'Bug Reports'
    { name: 'Feedback', icon: MessageCircle, color: 'bg-blue-500', path: '/console/categories/feedback' }, // Assuming MessageCircle is for 'Feedback'
  ];

  let { children } = $props();
  let activeMenu = $state('');

  // Determine activeMenu based on the current path
  $effect(() =>{
    const currentPath = $page.url.pathname;
    
    // alert(currentPath);
    if (currentPath.startsWith('/console/users')) {
      activeMenu = 'Users';
    } else if (currentPath.startsWith('/console/events')) {
      activeMenu = 'Events';
    } else if (currentPath.startsWith('/console/admin/research')) {
      activeMenu = 'Research';
    } else if (currentPath.startsWith('/console/groups')) {
      activeMenu = 'Groups';
    } else if (currentPath.startsWith('/console/about')) {
      activeMenu = 'About';
    } else {
      // Check categories
      const activeCategory = categories.find(cat => currentPath.startsWith(cat.path));
      if (activeCategory) {
        activeMenu = activeCategory.name;
      } else if (currentPath.startsWith('/console/all-categories')) {
        activeMenu = 'All categories';
      } else {
        activeMenu = ''; // Default or based on other logic
      }
    }
  });

  // Helper function to create navigation links, assuming you might want to navigate
  // For buttons that just set activeMenu, on:click is fine as is.
  // If actual navigation is needed, use <a> tags or programmatic navigation.
</script>

<div class="drawer lg:drawer-open bg-base-100 min-h-screen">
  <input id="my-drawer-2" type="checkbox" class="drawer-toggle" />
  <div class="drawer-content flex flex-col">
    <!-- Page content will be rendered here by SvelteKit -->
    {@render children()}
    <label for="my-drawer-2" class="btn btn-primary drawer-button lg:hidden fixed bottom-4 right-4 z-10">Open drawer</label>
  </div>
  <div class="drawer-side">
    <label for="my-drawer-2" aria-label="close sidebar" class="drawer-overlay"></label>
    <ul class="menu p-4 w-64 min-h-full bg-base-200 text-base-content">
      {#if $auth.user}
      <div class="pb-4 border-b border-base-300">
        <div class="flex items-center space-x-2">
        <UserAvatar
          tabindex={0}
          class="cursor-pointer size-8"
          src={$auth.user.prefs["avatarUrl"] || ''}
          alt={$auth.user.name}
          fallback={$auth.user.name.substring(0, 1).toUpperCase() || $auth.user.email?.substring(0, 2).toUpperCase()} >
        </UserAvatar>
    
          <div>
            <div class="font-semibold text-sm">{$auth.user.name || 'N/A'}</div>
            <div class="text-xs text-base-content/70">{$auth.user.email || 'N/A'}</div>
          </div>
        </div>
      </div>
      {/if}
      
      <button class="btn btn-outline btn-sm  w-42  justify-between my-4">
        <div class="flex gap-2">
          <Search class="w-4 h-4"/>Search

        </div>
        <div class="">
          <kbd class="kbd kbd-xs">Ctrl</kbd>
          <kbd class="kbd kbd-xs">k</kbd>
        </div>
      </button>
      <!-- Sidebar content here -->
      <li class="menu-title text-xs">Navigation</li>
      <li><a href="/console/admin/research" class:btn-active={activeMenu === 'Research'} class="btn btn-ghost justify-start"><FileSearch class="w-4 h-4"/> Research</a></li>
      <li><a href="/console/events" class:btn-active={activeMenu === 'Events'} class="btn btn-ghost justify-start"><BarChart2 class="w-4 h-4"/> Events</a></li>
      <li><a href="/console/users" class:btn-active={activeMenu === 'Users'} class="btn btn-ghost justify-start"><Users class="w-4 h-4"/> Users</a></li>
      <li><a href="/console/groups" class:btn-active={activeMenu === 'Groups'} class="btn btn-ghost justify-start"><Users class="w-4 h-4"/> Groups</a></li>
      <li><a href="/console/about" class:btn-active={activeMenu === 'About'} class="btn btn-ghost justify-start"><Info class="w-4 h-4"/> About</a></li>
      
      <li class="menu-title text-xs mt-4">Categories</li>
      {#each categories as category}
        <li>
          <a href={category.path} class:btn-active={activeMenu === category.name} class="btn btn-ghost justify-start">
            <svelte:component this={category.icon} class={`w-3 h-3 mr-1 p-0.5 rounded-sm ${category.color} text-white`} /> 
            {category.name}
          </a>
        </li>
      {/each}
      <li><a href="/console/all-categories" class:btn-active={activeMenu === 'All categories'} class="btn btn-ghost justify-start"><ListFilter class="w-4 h-4"/> All categories</a></li>

      <!-- <div class="mt-auto flex items-center justify-between p-2 border-t border-base-300">
        <button class="btn btn-ghost btn-sm p-1"><Settings class="w-5 h-5" /></button>
        <button class="btn btn-ghost btn-sm p-1"><Search class="w-5 h-5" /></button>
      </div> -->
    </ul>
  </div>
</div>
