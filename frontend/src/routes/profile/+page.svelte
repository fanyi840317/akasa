<script lang="ts">
    import { auth } from "$lib/stores/auth";
    import { goto } from "$app/navigation";
    import { onMount } from "svelte";
    import { fly } from "svelte/transition";
    import { UserAvatar } from "$lib/components/ui/avatar";
    
    // User state
    let user = $state<any>(null);
    let loading = $state(true);
    
    // Subscribe to auth store
    onMount(() => {
        const unsubscribe = auth.subscribe(state => {
            user = state.user;
            loading = state.loading;
            
            // Redirect to login if not authenticated
            if (!state.loading && !state.user) {
                goto("/login");
            }
        });
        
        return () => {
            unsubscribe();
        };
    });
    
    // Handle logout
    function handleLogout() {
        auth.logout();
        goto("/");
    }
</script>

{#if loading}
    <div class="min-h-screen flex items-center justify-center">
        <span class="loading loading-spinner loading-lg"></span>
    </div>
{:else if user}
    <div class="container mx-auto px-4 py-8" in:fly={{ y: 20, duration: 500 }}>
        <div class="card bg-base-100 shadow-xl">
            <div class="card-body">
                <div class="flex flex-col md:flex-row items-center gap-6">
                    <div class="avatar">
                        <div class="w-24 rounded-full">
                            {#if user.prefs?.avatar}
                                <UserAvatar 
                                    src={user.prefs.avatar} 
                                    alt={user.name} 
                                    fallback={user.name?.[0] || "U"}
                                    class="w-24 h-24"
                                />
                            {:else}
                                <div class="flex items-center justify-center bg-primary text-primary-content w-full h-full">
                                    <span class="text-2xl">{user.name?.[0] || "U"}</span>
                                </div>
                            {/if}
                        </div>
                    </div>
                    
                    <div>
                        <h1 class="text-2xl font-bold">{user.name}</h1>
                        <p class="text-base-content/70">{user.email}</p>
                    </div>
                </div>
                
                <div class="divider"></div>
                
                <div class="flex flex-col gap-4">
                    <h2 class="text-xl font-semibold">账户信息</h2>
                    
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <h3 class="text-sm font-medium text-base-content/70">用户ID</h3>
                            <p>{user.$id}</p>
                        </div>
                        
                        <div>
                            <h3 class="text-sm font-medium text-base-content/70">注册时间</h3>
                            <p>{new Date(user.$createdAt || Date.now()).toLocaleDateString()}</p>
                        </div>
                    </div>
                </div>
                
                <div class="card-actions justify-end mt-6">
                    <button class="btn btn-error" onclick={handleLogout}>
                        退出登录
                    </button>
                </div>
            </div>
        </div>
    </div>
{/if}
