<script lang="ts">
  import { _ } from 'svelte-i18n';
  import { Button } from "$lib/components/ui/button";
  import { Input } from "$lib/components/ui/input";
  import { Label } from "$lib/components/ui/label";
  import { Avatar, AvatarImage, AvatarFallback } from "$lib/components/ui/avatar";
  import { Camera } from "lucide-svelte";

  let avatarFile: File | null = null;
  let avatarPreview: string | null = null;
  let username = "";
  let email = "";
  let bio = "";

  function handleAvatarChange(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
      avatarFile = input.files[0];
      avatarPreview = URL.createObjectURL(avatarFile);
    }
  }

  async function handleSubmit() {
    // TODO: 实现保存个人信息的逻辑
    console.log('保存个人信息', { username, email, bio, avatarFile });
  }
</script>

<div class="space-y-6">
  <div class="flex items-center justify-between mb-6">
    <div>
      <h3 class="text-lg font-medium">{$_('profile.personal_info')}</h3>
      <p class="text-sm text-muted-foreground">{$_('profile.personal_info_desc')}</p>
    </div>
    <Button variant="destructive" size="sm" on:click={() => {
      // TODO: 实现退出登录逻辑
      console.log('退出登录');
    }}>
      {$_('auth.logout')}
    </Button>
  </div>

  <form on:submit|preventDefault={handleSubmit} class="space-y-8">
    <div class="space-y-4">
      <!-- 头像上传 -->
      <div class="flex items-center gap-4">
        <Avatar class="h-24 w-24">
          {#if avatarPreview}
            <AvatarImage src={avatarPreview} alt="Avatar" />
          {:else}
            <AvatarFallback class="text-lg">{username ? username[0].toUpperCase() : 'U'}</AvatarFallback>
          {/if}
        </Avatar>
        <div class="space-y-2">
          <Label for="avatar" class="inline-block">
            <div class="flex items-center gap-2 cursor-pointer">
              <Button type="button" variant="outline" size="sm">
                <Camera class="h-4 w-4 mr-2" />
                {$_('profile.change_avatar')}
              </Button>
            </div>
          </Label>
          <input
            type="file"
            id="avatar"
            accept="image/*"
            class="hidden"
            on:change={handleAvatarChange}
          />
          <p class="text-xs text-muted-foreground">{$_('profile.avatar_requirements')}</p>
        </div>
      </div>

      <!-- 用户名 -->
      <div class="space-y-2">
        <Label for="username">{$_('profile.username')}</Label>
        <Input
          type="text"
          id="username"
          bind:value={username}
          placeholder={$_('profile.username_placeholder')}
        />
      </div>

      <!-- 邮箱 -->
      <div class="space-y-2">
        <Label for="email">{$_('profile.email')}</Label>
        <Input
          type="email"
          id="email"
          bind:value={email}
          placeholder={$_('profile.email_placeholder')}
        />
      </div>

      <!-- 个人简介 -->
      <div class="space-y-2">
        <Label for="bio">{$_('profile.bio')}</Label>
        <textarea
          id="bio"
          bind:value={bio}
          rows="4"
          class="w-full min-h-[80px] rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
          placeholder={$_('profile.bio_placeholder')}
        />
      </div>
    </div>

    <Button type="submit">{$_('common.save')}</Button>
  </form>
</div>