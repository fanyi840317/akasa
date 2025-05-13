<script lang="ts">
  import { auth } from "$lib/stores/auth";
  import { goto } from "$app/navigation";
  import { fly } from "svelte/transition";
  import { UserPlus, User, KeyRound, AlertCircle } from "lucide-svelte";
  import { base } from "$app/paths";
  import { page } from "$app/stores";
  import { toast } from "svelte-sonner";

  // 从URL获取returnUrl参数
  let returnUrl = $page.url.searchParams.get("returnUrl");

  // Form state
  let email = $state(""); // In the image, this is used as username
  let password = $state("");
  // let username = $state(""); // username field is not explicitly separate in the image for register
  let isRegister = $state(false); // Default to register form to match image
  let loading = $state(false);
  let error = $state("");

  let acceptTerms = $state(false);
  let subscribeSpam = $state(false);

  // Toggle between login and register forms
  function toggleForm() {
    isRegister = !isRegister;
    error = "";
  }

  // Handle form submission
  async function handleSubmit() {
    error = "";
    loading = true;
    // let user = null;

    try {
      if (isRegister) {
        // Assuming 'email' state is used for username as per image
        if (!email) {
          // Changed from username to email for the first field
          error = "Username cannot be empty";
          loading = false;
          return;
        }
        if (password.length < 8) {
          error = "Password must be 8+ characters";
          loading = false;
          return;
        }
        // Using email as username for registration as per image context
        await auth.register(email, password, email);
      } else {
        await auth.login(email, password);
      }

      // 重定向到指定页面或首页
      // 统一重定向逻辑
      if (returnUrl) {
        await goto(`${base}${returnUrl}`);
      } else {
        await goto(`${base}/console`);
      }
    } catch (err: any) {
      error =
        err.message ||
        (isRegister
          ? "Registration failed, please try again"
          : "Login failed, please try again");

      // 显示错误信息
      toast.error(err.message);
    } finally {
      loading = false;
    }
  }
</script>

<style>
  input:-webkit-autofill,
  input:-webkit-autofill:hover,
  input:-webkit-autofill:focus,
  input:-webkit-autofill:active {
    -webkit-box-shadow: 0 0 0 30px hsl(var(--b1)) inset !important;
    -webkit-text-fill-color: hsl(var(--bc)) !important;
    caret-color: hsl(var(--bc)) !important;
  }

  /* Firefox specific override if needed, though box-shadow trick is often enough */
  /* input:-moz-autofill {
    box-shadow: 0 0 0 30px hsl(var(--b1)) inset !important;
    -webkit-text-fill-color: hsl(var(--bc)) !important; Firefox might not respect -webkit-text-fill-color
    color: hsl(var(--bc)) !important; 
    caret-color: hsl(var(--bc)) !important;
  } */

  /* A more standard approach, though -webkit-prefixed is widely supported */
  /* input:autofill {
    box-shadow: 0 0 0 30px hsl(var(--b1)) inset !important;
    -webkit-text-fill-color: hsl(var(--bc)) !important;
    color: hsl(var(--bc)) !important;
    caret-color: hsl(var(--bc)) !important;
  } */

  /* DaisyUI input fields might need specific targeting if the above is too general */
  .input:-webkit-autofill,
  .input:-webkit-autofill:hover,
  .input:-webkit-autofill:focus,
  .input:-webkit-autofill:active {
    -webkit-box-shadow: 0 0 0 30px hsl(var(--b1)) inset !important;
    -webkit-text-fill-color: hsl(var(--bc)) !important;
    caret-color: hsl(var(--bc)) !important;
  }
</style>


<div
  class="min-h-screen flex items-center justify-center bg-base-200 p-4"
  in:fly={{ y: 20, duration: 500 ,delay:800}}
>
  <div class="card w-full max-w-md bg-base-100 shadow-xl"  >
    <div class="card-body">
      {#if !isRegister}
        <div class="flex items-center gap-2 mb-1">
          <UserPlus class="w-6 h-6" />
          <h2 class="card-title text-xl font-semibold">Create new account</h2>
        </div>
        <p class="text-sm text-base-content/70 mb-6">
          Registration is free and only takes a minute
        </p>
      {:else}
        <div class="flex items-center gap-2 mb-1">
          <User class="w-6 h-6" />
          <h2 class="card-title text-xl font-semibold">
            Login to your account
          </h2>
        </div>
        <p class="text-sm text-base-content/70 mb-6">
          Welcome back! Please enter your details.
        </p>
      {/if}

      <!-- {#if error}
        <div class="alert alert-error mb-4 text-sm p-3">
          <AlertCircle class="w-4 h-4 mr-1" />
          <span>{error}</span>
        </div>
      {/if} -->

      <form onsubmit={handleSubmit} class="space-y-4">
        {#if isRegister}
          <!-- Corrected condition: show register form when isRegister is true -->

          <!-- Username/Email input -->
          <label class="input input-bordered flex items-center gap-2 w-full">
            <User class="w-4 h-4 text-base-content/50" />
            <input
              type="text"
              class="grow"
              placeholder="Username or Email"
              bind:value={email}
              required
            />
          </label>

          <!-- Password input -->
          <label class="input input-bordered flex items-center gap-2 w-full">
            <KeyRound class="w-4 h-4 text-base-content/50" />
            <input
              type="password"
              class="grow"
              placeholder="••••••"
              bind:value={password}
              required
            />
          </label>

          <p class="text-xs text-error flex items-center mt-1 ml-2">
            <AlertCircle class="w-3 h-3 mr-1" />
            Password must be 8+ characters
          </p>

          <div class="form-control mt-2">
            <label class="label">
              <input
                type="checkbox"
                bind:checked={acceptTerms}
                class="toggle toggle-xs"
              />
              Accept terms without reading
            </label>
          </div>

          <div class="form-control">
            <label class="label">
              <input
                type="checkbox"
                bind:checked={subscribeSpam}
                class="toggle toggle-xs"
              />
              Subscribe to spam emails
            </label>
          </div>

          <div class="form-control mt-6">
            <button
              type="submit"
              class="btn btn-neutral btn-block"
              disabled={loading}
            >
              {#if loading}
                <span class="loading loading-spinner loading-sm"></span>
              {/if}
              Register
            </button>
          </div>
        {:else}
          <!-- Login Form -->
          <!-- <label class="floating-label">
            <span>Your Email or Username</span>
            <input
              type="text"
              placeholder="Email or Username"
              bind:value={email}
              class="input input-md w-full"
            />
          </label> -->

          <label class="input input-bordered flex items-center gap-2 w-full">
            <User class="w-4 h-4 text-base-content/50" />
            <input
              type="email"
              class="grow"
              placeholder="Email or Username"
              bind:value={email}
              required
            />
          </label>
          <!-- <label class="floating-label">
            <span>Password</span>
            <input
              type="text"
              placeholder="Password"
              bind:value={password}
              class="input input-md w-full"
            />
          </label> -->
          <label class="input input-bordered flex items-center gap-2 w-full">
            <KeyRound class="w-4 h-4 text-base-content/50" />
            <input
              type="password"
              class="grow"
              placeholder="Password"
              bind:value={password}
              required
            />
          </label>
          {#if error}
            <p class="text-xs text-error flex items-center mt-1 ml-2">
              <AlertCircle class="w-3 h-3 mr-1" />
              {error}
            </p>
          {/if}
          <div class="form-control mt-6">
            <button
              type="submit"
              class="btn btn-neutral btn-block"
              disabled={loading}
            >
              {#if loading}
                <span class="loading loading-spinner loading-sm"></span>
              {/if}
              Login
            </button>
          </div>
        {/if}
      </form>

      <div class="text-center mt-6">
        <button
          class="btn btn-link btn-sm normal-case font-normal text-base-content/80 hover:text-base-content"
          onclick={toggleForm}
        >
          {isRegister ? "Or login" : "Or create new account"}
        </button>
      </div>
    </div>
  </div>
</div>
