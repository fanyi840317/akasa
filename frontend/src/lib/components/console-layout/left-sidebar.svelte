<script>
  import { Search, BarChart2, MapIcon, ListFilter, MessageSquare, HelpCircle, Lightbulb } from "lucide-svelte";
  import CategoryNavItem from "../ui/nav/category-nav-item.svelte";
  import NavItem from "../ui/nav/nav-item.svelte";
  import { cn } from "$lib/utils";

  // 接收从父组件传递的 props
  let {
    activeMenu = "",
    categories =[],
    class:className = "",
  } = $props();
</script>
<div class={cn("flex flex-col h-full overflow-hidden",className)}>
    <ul
      class="menu py-10 w-64 text-base-content/50 gap-2 flex-1
      items-start justify-start
       overflow-y-auto overflow-x-hidden"
    >
      <div class="mb-6 px-6">
        <h1
          class="text-3xl font-bold text-center bg-clip-text
          text-transparent bg-gradient-to-br from-primary via-accent to-secondary
          tracking-tight"
        >
          Akasa
        </h1>
        <div
          class="w-16 h-0.5 bg-gradient-to-r from-primary to-accent mx-auto mt-2 rounded-full opacity-60"
        ></div>
      </div>
      <div class="w-full flex-1 px-5">
        <!-- Sidebar content here -->
        <!-- 新建按钮 -->

        <!-- 搜索按钮 -->
        <button
          class="w-full mb-6 px-4 py-3 bg-base-200/50 hover:bg-base-200
                 text-base-content/70 hover:text-base-content rounded-xl
                 font-medium text-sm transition-all duration-200
                 hover:scale-[1.02] hover:shadow-md
                 flex items-center justify-center gap-2 group"
        >
          <Search
            class="w-4 h-4 group-hover:scale-110 transition-transform duration-200"
          />
          搜索
          <span class="ml-auto text-xs opacity-50 kbd kbd-xs">Ctrl</span>
          <span class="text-xs opacity-50 kbd kbd-xs">K</span>
        </button>

        <div class="mb-6">
          <div class="flex items-center gap-2 mb-3 px-2">
            <div
              class="w-1 h-4 bg-gradient-to-b from-primary to-accent rounded-full"
            ></div>
            <span
              class="menu-title text-xs font-semibold text-base-content/70 tracking-wider uppercase"
              >Navigation</span
            >
          </div>
        </div>

        <!-- <NavItem
          href="/console/admin/research"
          icon={FileSearch}
          label="Research"
          isActive={activeMenu === "Research"}
        /> -->

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

        <!-- <NavItem
          href="/console/groups"
          icon={Users}
          label="Groups"
          isActive={activeMenu === "Groups"}
        />

        <NavItem
          href="/console/about"
          icon={Info}
          label="About"
          isActive={activeMenu === "About"}
        /> -->

        <div class="mt-8 mb-6">
          <div class="flex items-center gap-2 mb-3 px-2">
            <div
              class="w-1 h-4 bg-gradient-to-b from-accent to-secondary rounded-full"
            ></div>
            <span
              class="menu-title text-xs font-semibold text-base-content/70 tracking-wider uppercase"
              >Categories</span
            >
          </div>
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