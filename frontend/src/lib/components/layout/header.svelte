<script lang="ts">
  import { UserAvatar } from "../ui/avatar";
  import { goto } from "$app/navigation";
  import { LogInIcon, UserCircle, LogOut, Settings } from "lucide-svelte";
  import { cn } from "$lib/utils";
  import { fly } from "svelte/transition";

  // Define user type
  type UserData = {
    name: string;
    avatar?: string;
    email?: string;
  } | null;

  let {
    user = null,
    onLogin = () => {},
    onLogout = () => {},
    onProfile = () => {},
    onSettings = () => {},
    class: className = "",
    isShow = $bindable(true),
  } = $props<{
    user?: UserData;
    onLogin?: () => void;
    onLogout?: () => void;
    onProfile?: () => void;
    onSettings?: () => void;
    class?: string;
    isShow?: boolean;
  }>();
</script>

{#if isShow}
  <div class={cn("navbar backdrop-blur-sm shadow-sm", className)}>
    <div class="navbar-start">
      <button
        class="btn btn-ghost text-xl"
        onclick={() => goto("/")}
        onkeydown={(e) => e.key === "Enter" && goto("/")}
      >
        Akasa
      </button>
    </div>
    <div class="navbar-end">
      {#if user}
        <!-- User is logged in -->
        <div class="dropdown dropdown-end">
          <UserAvatar
            tabindex={0}
            class="cursor-pointer rounded-full"
            src={user.avatar}
            alt={user.name}
            fallback={user.name?.[0] || "U"}
          />
          <ul
            role="menu"
            class="mt-1 z-[1]  shadow menu menu-md dropdown-content gap-2
					bg-base-300 rounded-lg w-46"
          >
            <li>
              <button onclick={onProfile} class="flex items-center gap-2">
                <UserCircle class="h-4 w-4" />
                个人资料
              </button>
            </li>
            <li>
              <button onclick={onSettings} class="flex items-center gap-2">
                <Settings class="h-4 w-4" />
                设置
              </button>
            </li>
            <li>
              <button
                class="flex items-center gap-2"
                onclick={onLogout}
                onkeydown={(e) => e.key === "Enter" && onLogout()}
              >
                <LogOut class="h-4 w-4" />
                退出登录
              </button>
            </li>
          </ul>
        </div>
      {:else}
        <!-- User is not logged in -->
        <button
          class="btn gap-2 btn-ghost"
          onclick={onLogin}
          onkeydown={(e) => e.key === "Enter" && onLogin()}
        >
          <LogInIcon class="h-4 w-4" />
          <span>登录</span>
        </button>
      {/if}
    </div>
  </div>
{/if}
