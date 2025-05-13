<script lang="ts">
  import { Users, BarChart2, Shield, MessageSquare, Info, Settings, Search, ChevronDown, Heart, MessageCircle, Eye, Calendar, ThumbsUp, ThumbsDown, FileText, Tag, ListFilter } from 'lucide-svelte';
  import { UserAvatar } from '$lib/components/ui/avatar';

  // Mock data - replace with actual data fetching
  const users = [
    { id: 1, username: 'qwert', name: 'lonser', avatar: 'https://i.pravatar.cc/40?u=qwert', received: 56, given: 5, topicsCreated: 6, repliesPosted: 25, topicsViewed: 108, postsRead: 521, daysVisited: 7 },
    { id: 2, username: 'NuBathTech', name: 'George', avatar: 'https://i.pravatar.cc/40?u=NuBathTech', received: 44, given: 1, topicsCreated: 2, repliesPosted: 2, topicsViewed: 6, postsRead: 14, daysVisited: 2 },
    { id: 3, username: 'stdnt_aryo', name: '', avatar: null, fallback: 'S', received: 44, given: 0, topicsCreated: 1, repliesPosted: 0, topicsViewed: 4, postsRead: 12, daysVisited: 1 },
    { id: 4, username: 'deanrie', name: 'Dean Rie', avatar: 'https://i.pravatar.cc/40?u=deanrie', received: 24, given: 15, topicsCreated: 0, repliesPosted: 70, topicsViewed: 476, postsRead: '2.1k', daysVisited: 7 },
    { id: 5, username: 'danperks', name: 'Dan', subtitle: 'Community Developer', avatar: 'https://i.pravatar.cc/40?u=danperks', received: 19, given: 0, topicsCreated: 0, repliesPosted: 38, topicsViewed: 48, postsRead: 288, daysVisited: 5 },
    { id: 6, username: 'WraithIT', name: 'Wraith', avatar: 'https://i.pravatar.cc/40?u=WraithIT', received: 16, given: 0, topicsCreated: 1, repliesPosted: 0, topicsViewed: 30, postsRead: 118, daysVisited: 6 },
    { id: 7, username: 'AbleArcher', name: '', avatar: 'https://i.pravatar.cc/40?u=AbleArcher', received: 14, given: 4, topicsCreated: 1, repliesPosted: 9, topicsViewed: 12, postsRead: 103, daysVisited: 6 },
    { id: 8, username: 'cocode', name: 'Babak Bandpey', avatar: 'https://i.pravatar.cc/40?u=cocode', received: 13, given: 8, topicsCreated: 1, repliesPosted: 9, topicsViewed: 8, postsRead: 73, daysVisited: 4 },
  ];

  const categories = [
    { name: 'Discussion', icon: MessageSquare, color: 'bg-blue-500' },
    { name: 'How To', icon: FileText, color: 'bg-orange-500' },
    { name: 'Feature Requests', icon: ThumbsUp, color: 'bg-green-500' },
    { name: 'Bug Reports', icon: ThumbsDown, color: 'bg-purple-500' },
    { name: 'Feedback', icon: MessageCircle, color: 'bg-blue-500' },
  ];

  let searchTerm = '';
  let activeMenu = 'Users';

  function formatK(num: number | string) {
    if (typeof num === 'string' && num.endsWith('k')) return num;
    if (typeof num === 'number' && num >= 1000) {
      return (num / 1000).toFixed(1) + 'k';
    }
    return num;
  }
</script>

<div class="drawer lg:drawer-open bg-base-100 min-h-screen">
  <input id="my-drawer-2" type="checkbox" class="drawer-toggle" />
  <div class="drawer-content flex flex-col">
    <!-- Page content here -->
    <div class="p-6">
      <div class="flex justify-between items-center mb-4">
        <div class="flex items-center gap-2">
          <h1 class="text-2xl font-semibold">Week MAY 7 - MAY 13</h1>
          <button class="btn btn-ghost btn-sm p-1">
            <ChevronDown class="w-5 h-5" />
          </button>
        </div>
        <div class="flex items-center gap-4">
          <span class="text-sm text-base-content/70">42182 users</span>
          <div class="form-control">
            <input type="text" placeholder="filter by username" class="input input-bordered input-sm w-full max-w-xs" bind:value={searchTerm} />
          </div>
        </div>
      </div>
      <p class="text-xs text-base-content/60 mb-6">Last Updated: May 12, 2025 12:06 pm</p>

      <!-- Users Table -->
      <div class="overflow-x-auto">
        <table class="table table-zebra w-full">
          <thead>
            <tr class="text-base-content/80">
              <th>Username</th>
              <th class="cursor-pointer hover:text-base-content">
                <div class="flex items-center gap-1">
                  <Heart class="w-4 h-4 text-error" /> Received <ChevronDown class="w-4 h-4" />
                </div>
              </th>
              <th><div class="flex items-center gap-1"><Heart class="w-4 h-4 text-success" /> Given</div></th>
              <th>Topics Created</th>
              <th>Replies Posted</th>
              <th>Topics Viewed</th>
              <th>Posts Read</th>
              <th>Days Visited</th>
            </tr>
          </thead>
          <tbody>
            {#each users.filter(u => u.username.toLowerCase().includes(searchTerm.toLowerCase())) as user (user.id)}
              <tr>
                <td>
                  <div class="flex items-center space-x-3">
                    <UserAvatar src={user.avatar} alt={user.username} fallback={user.fallback || user.username[0].toUpperCase()} class="w-10 h-10" />
                    <div>
                      <div class="font-bold">{user.username}</div>
                      <div class="text-sm opacity-50">{user.name}</div>
                      {#if user.subtitle}
                        <div class="text-xs opacity-50">{user.subtitle}</div>
                      {/if}
                    </div>
                  </div>
                </td>
                <td>{user.received}</td>
                <td>{user.given}</td>
                <td>{user.topicsCreated}</td>
                <td>{user.repliesPosted}</td>
                <td>{user.topicsViewed}</td>
                <td>{formatK(user.postsRead)}</td>
                <td>{user.daysVisited}</td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    </div>
    <label for="my-drawer-2" class="btn btn-primary drawer-button lg:hidden fixed bottom-4 right-4 z-10">Open drawer</label>
  </div>
  <div class="drawer-side">
    <label for="my-drawer-2" aria-label="close sidebar" class="drawer-overlay"></label>
    <ul class="menu p-4 w-64 min-h-full bg-base-200 text-base-content">
      <!-- Sidebar content here -->
      <li class="menu-title text-xs">Navigation</li>
      <li><button class:btn-active={activeMenu === 'Topics'} on:click={() => activeMenu = 'Topics'} class="btn btn-ghost justify-start"><BarChart2 class="w-4 h-4"/> Topics</button></li>
      <li><button class:btn-active={activeMenu === 'Users'} on:click={() => activeMenu = 'Users'} class="btn btn-ghost justify-start"><Users class="w-4 h-4"/> Users</button></li>
      <li><button class:btn-active={activeMenu === 'Badges'} on:click={() => activeMenu = 'Badges'} class="btn btn-ghost justify-start"><Shield class="w-4 h-4"/> Badges</button></li>
      <li><button class:btn-active={activeMenu === 'Groups'} on:click={() => activeMenu = 'Groups'} class="btn btn-ghost justify-start"><Users class="w-4 h-4"/> Groups</button></li>
      <li><button class:btn-active={activeMenu === 'About'} on:click={() => activeMenu = 'About'} class="btn btn-ghost justify-start"><Info class="w-4 h-4"/> About</button></li>
      
      <li class="menu-title text-xs mt-4">Categories</li>
      {#each categories as category}
        <li>
          <button class="btn btn-ghost justify-start">
            <svelte:component this={category.icon} class={`w-3 h-3 mr-1 p-0.5 rounded-sm ${category.color} text-white`} /> 
            {category.name}
          </button>
        </li>
      {/each}
      <li><button class="btn btn-ghost justify-start"><ListFilter class="w-4 h-4"/> All categories</button></li>

      <div class="mt-auto flex items-center justify-between p-2 border-t border-base-300">
        <button class="btn btn-ghost btn-sm p-1"><Settings class="w-5 h-5" /></button>
        <button class="btn btn-ghost btn-sm p-1"><Search class="w-5 h-5" /></button>
      </div>
    </ul>
  </div>
</div>