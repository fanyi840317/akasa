<script lang="ts">
    import { auth } from "$lib/stores/auth";
    import { goto } from "$app/navigation";
    import { fly } from "svelte/transition";
    
    // Form state
    let email = $state("");
    let password = $state("");
    let username = $state("");
    let isRegister = $state(false);
    let loading = $state(false);
    let error = $state("");
    
    // Toggle between login and register forms
    function toggleForm() {
        isRegister = !isRegister;
        error = "";
    }
    
    // Handle form submission
    async function handleSubmit() {
        error = "";
        loading = true;
        
        try {
            if (isRegister) {
                if (!username) {
                    error = "用户名不能为空";
                    loading = false;
                    return;
                }
                
                await auth.register(email, password, username);
            } else {
                await auth.login(email, password);
            }
            
            // Redirect to home page on success
            goto("/");
        } catch (err: any) {
            error = err.message || "登录失败，请重试";
        } finally {
            loading = false;
        }
    }
    
    // Mock login for demo purposes
    function handleMockLogin() {
        const mockUser = {
            $id: "mock-user-id",
            name: "测试用户",
            email: "test@example.com",
            prefs: {
                avatar: "https://api.dicebear.com/7.x/bottts/svg?seed=demo"
            }
        };
        
        auth.setUser(mockUser);
        goto("/");
    }
</script>

<div class="min-h-screen flex items-center justify-center bg-base-200" in:fly={{ y: 20, duration: 500 }}>
    <div class="card w-full max-w-md bg-base-100 shadow-xl">
        <div class="card-body">
            <h2 class="card-title text-2xl font-bold text-center mb-6">
                {isRegister ? "注册账号" : "登录账户"}
            </h2>
            
            {#if error}
                <div class="alert alert-error mb-4">
                    <span>{error}</span>
                </div>
            {/if}
            
            <form on:submit|preventDefault={handleSubmit} class="space-y-4">
                {#if isRegister}
                    <div class="form-control">
                        <label class="label">
                            <span class="label-text">用户名</span>
                        </label>
                        <input 
                            type="text" 
                            placeholder="输入用户名" 
                            class="input input-bordered" 
                            bind:value={username}
                            required
                        />
                    </div>
                {/if}
                
                <div class="form-control">
                    <label class="label">
                        <span class="label-text">邮箱</span>
                    </label>
                    <input 
                        type="email" 
                        placeholder="输入邮箱" 
                        class="input input-bordered" 
                        bind:value={email}
                        required
                    />
                </div>
                
                <div class="form-control">
                    <label class="label">
                        <span class="label-text">密码</span>
                    </label>
                    <input 
                        type="password" 
                        placeholder="输入密码" 
                        class="input input-bordered" 
                        bind:value={password}
                        required
                    />
                </div>
                
                <div class="form-control mt-6">
                    <button 
                        type="submit" 
                        class="btn btn-primary" 
                        disabled={loading}
                    >
                        {#if loading}
                            <span class="loading loading-spinner loading-sm"></span>
                        {/if}
                        {isRegister ? "注册" : "登录"}
                    </button>
                </div>
            </form>
            
            <div class="divider">或者</div>
            
            <button 
                class="btn btn-outline btn-block" 
                onclick={handleMockLogin}
                disabled={loading}
            >
                模拟登录（测试用）
            </button>
            
            <div class="text-center mt-4">
                <button 
                    class="btn btn-link btn-sm" 
                    onclick={toggleForm}
                >
                    {isRegister ? "已有账号？点击登录" : "没有账号？点击注册"}
                </button>
            </div>
        </div>
    </div>
</div>
