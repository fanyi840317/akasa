<script lang="ts">
  import { _ } from 'svelte-i18n';
  import { Button } from "$lib/components/ui/button";
  import { Label } from "$lib/components/ui/label";
  import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "$lib/components/ui/select";
  import { Switch } from "$lib/components/ui/switch";
  import { Moon, Sun, Globe } from "lucide-svelte";

  let darkMode = false;
  let language = 'zh';
  let emailNotifications = true;
  let pushNotifications = true;

  function toggleTheme() {
    darkMode = !darkMode;
    // TODO: 实现主题切换逻辑
  }

  function handleLanguageChange(value: string) {
    language = value;
    // TODO: 实现语言切换逻辑
  }

  function handleNotificationChange() {
    // TODO: 实现通知设置保存逻辑
  }
</script>

<div class="space-y-6">
  <div>
    <h3 class="text-lg font-medium">{$_('profile.settings')}</h3>
    <p class="text-sm text-muted-foreground">{$_('profile.settings_desc')}</p>
  </div>

  <div class="space-y-8">
    <!-- 主题设置 -->
    <div class="flex items-center justify-between">
      <div class="space-y-0.5">
        <Label>{$_('settings.theme')}</Label>
        <p class="text-sm text-muted-foreground">{$_('settings.theme_desc')}</p>
      </div>
      <Button variant="outline" size="icon" on:click={toggleTheme}>
        {#if darkMode}
          <Moon class="h-5 w-5" />
        {:else}
          <Sun class="h-5 w-5" />
        {/if}
      </Button>
    </div>

    <!-- 语言设置 -->
    <div class="flex items-center justify-between">
      <div class="space-y-0.5">
        <Label>{$_('settings.language')}</Label>
        <p class="text-sm text-muted-foreground">{$_('settings.language_desc')}</p>
      </div>
      <Select value={language} onValueChange={handleLanguageChange}>
        <SelectTrigger class="w-[200px]">
          <Globe class="mr-2 h-4 w-4" />
          <SelectValue placeholder={$_('settings.select_language')} />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="zh">中文</SelectItem>
          <SelectItem value="en">English</SelectItem>
        </SelectContent>
      </Select>
    </div>

    <!-- 通知设置 -->
    <div class="space-y-4">
      <div class="space-y-0.5">
        <Label>{$_('settings.notifications')}</Label>
        <p class="text-sm text-muted-foreground">{$_('settings.notifications_desc')}</p>
      </div>
      <div class="space-y-4">
        <div class="flex items-center justify-between">
          <Label for="email-notifications" class="flex flex-col space-y-1">
            <span>{$_('settings.email_notifications')}</span>
            <span class="text-sm font-normal text-muted-foreground">
              {$_('settings.email_notifications_desc')}
            </span>
          </Label>
          <Switch
            id="email-notifications"
            checked={emailNotifications}
            on:change={handleNotificationChange}
          />
        </div>
        <div class="flex items-center justify-between">
          <Label for="push-notifications" class="flex flex-col space-y-1">
            <span>{$_('settings.push_notifications')}</span>
            <span class="text-sm font-normal text-muted-foreground">
              {$_('settings.push_notifications_desc')}
            </span>
          </Label>
          <Switch
            id="push-notifications"
            checked={pushNotifications}
            on:change={handleNotificationChange}
          />
        </div>
      </div>
    </div>
  </div>
</div>