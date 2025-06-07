<script>
  import { Search, BarChart2, MapIcon, ListFilter, PlusCircle, MessageSquare, HelpCircle, Lightbulb, Bot } from "lucide-svelte";
  import CategoryNavItem from "../ui/nav/category-nav-item.svelte";
  import NavItem from "../ui/nav/nav-item.svelte";
  import { cn } from "$lib/utils";
    import { AddCursorIcon } from "@blocksuite/icons/lit";
  // import SearchButton from "../ui/buttons/search-button.svelte";

  // 接收从父组件传递的 props
  let {
    activeMenu = "",
    categories =[],
    class:className = "",
  } = $props();
</script>
<div class={cn("flex flex-col h-full overflow-hidden",className)}>
    <ul
      class="py-4 w-54 px-4 text-base-content/50 gap-2 flex-1
      items-start justify-start
       overflow-y-auto overflow-x-hidden"
    >
    
      <div class="flex-1 flex flex-col">
        <!-- Sidebar content here -->
        <!-- 新建按钮 -->

        <!-- 搜索按钮 -->
        <!-- <SearchButton class="mb-2" onClick={() => console.log('Search clicked')} /> -->

        <div class="flex items-center gap-2 mb-2">
          <!-- <div
            class="w-1 h-4 bg-gradient-to-b from-primary to-accent rounded-full"
          ></div> -->
          <span
            class="menu-title text-xs font-semibold text-base-content/70 tracking-wider uppercase"
            >Navigation</span
          >
        </div>

        <NavItem
          href="/console/admin/research"
          icon={PlusCircle}
          label="Create"
          isActive={activeMenu === "Research"}
        />

        <NavItem
          href="/console/events"
          icon={BarChart2}
          label="Explore"
          isActive={activeMenu === "Explore"}
        />

        <NavItem
          href="/console/users"
          icon={MapIcon}
          label="Map"
          isActive={activeMenu === "Users"}
        />

       

        <div class="flex items-center gap-2 my-4">
          <!-- <div
            class="w-1 h-4 bg-gradient-to-b from-accent to-secondary rounded-full"
          ></div> -->
          <span
            class="menu-title text-xs font-semibold text-base-content/70 tracking-wider uppercase"
            >Categories</span
          >
        </div>
        {#each categories as category}
          <CategoryNavItem
            href={category.path}
            icon={category.icon}
            label={category.name}
            color={category.color}
            isActive={activeMenu === category.name}
          />
        {/each}

        <NavItem
          href="/console/all-categories"
          icon={ListFilter}
          label="All categories"
          isActive={activeMenu === "All categories"}
          class="btn-ghost"
        />
      </div>
    </ul>
  </div>