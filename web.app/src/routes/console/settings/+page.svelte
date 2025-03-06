<script lang="ts">
    /**
     * 控制台设置页面
     * 提供Notion风格的用户设置界面
     */
    import { Header, PageContent, NotionCard } from "$lib/components/console";
    import { notionClass } from "$lib/components/console/styles";
    import { Switch } from "$lib/components/ui/switch";
    import { Button } from "$lib/components/ui/button";
    import { Separator } from "$lib/components/ui/separator";
    import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "$lib/components/ui/select";
    import { Input } from "$lib/components/ui/input";
    import { Label } from "$lib/components/ui/label";
    import { Globe, Moon, Sun, User, Bell, HelpCircle, Shield } from "lucide-svelte";
    import { theme } from "$lib/stores/theme";
    import { _ } from "svelte-i18n";
</script>

<Header title={$_("settings.title")} subtitle={$_("settings.subtitle")} />

<PageContent class="max-w-4xl mx-auto">
    <div class="grid grid-cols-1 md:grid-cols-[250px_1fr] gap-6">
        <!-- 设置导航 -->
        <div class="space-y-1">
            <Button variant="ghost" class="w-full justify-start" size="sm">
                <User class="h-4 w-4 mr-2" />
                {$_("settings.account")}
            </Button>
            <Button variant="ghost" class="w-full justify-start" size="sm">
                <Bell class="h-4 w-4 mr-2" />
                {$_("settings.notifications")}
            </Button>
            <Button variant="ghost" class="w-full justify-start bg-accent" size="sm">
                <Globe class="h-4 w-4 mr-2" />
                {$_("settings.appearance")}
            </Button>
            <Button variant="ghost" class="w-full justify-start" size="sm">
                <Shield class="h-4 w-4 mr-2" />
                {$_("settings.privacy")}
            </Button>
            <Button variant="ghost" class="w-full justify-start" size="sm">
                <HelpCircle class="h-4 w-4 mr-2" />
                {$_("settings.help")}
            </Button>
        </div>
        
        <!-- 设置内容 -->
        <div class="space-y-6">
            <NotionCard title={$_("settings.appearance.title")} subtitle={$_("settings.appearance.subtitle")}>
                <div class="space-y-4">
                    <!-- 主题设置 -->
                    <div class="space-y-2">
                        <Label class="text-base font-medium">{$_("settings.appearance.theme")}</Label>
                        <div class="flex flex-wrap gap-3">
                            <button 
                                class="flex flex-col items-center justify-center border rounded-lg p-3 w-24 h-24 
                                       {theme === 'light' ? 'border-primary bg-accent' : 'border-muted-foreground/20'}"
                                on:click={() => ($theme = 'light')}
                            >
                                <Sun class="h-10 w-10 mb-2" />
                                <span class="text-sm font-medium">{$_("settings.appearance.light")}</span>
                            </button>
                            
                            <button 
                                class="flex flex-col items-center justify-center border rounded-lg p-3 w-24 h-24 
                                       {theme === 'dark' ? 'border-primary bg-accent' : 'border-muted-foreground/20'}"
                                on:click={() => ($theme = 'dark')}
                            >
                                <Moon class="h-10 w-10 mb-2" />
                                <span class="text-sm font-medium">{$_("settings.appearance.dark")}</span>
                            </button>
                            
                            <button 
                                class="flex flex-col items-center justify-center border rounded-lg p-3 w-24 h-24 
                                       {theme === 'system' ? 'border-primary bg-accent' : 'border-muted-foreground/20'}"
                                on:click={() => ($theme = 'system')}
                            >
                                <div class="h-10 w-10 mb-2 flex">
                                    <Sun class="h-5 w-5" />
                                    <Moon class="h-5 w-5" />
                                </div>
                                <span class="text-sm font-medium">{$_("settings.appearance.system")}</span>
                            </button>
                        </div>
                    </div>
                    
                    <Separator />
                    
                    <!-- 语言设置 -->
                    <div class="space-y-2">
                        <Label class="text-base font-medium">{$_("settings.appearance.language")}</Label>
                        <Select defaultValue="zh">
                            <SelectTrigger class="w-full max-w-xs">
                                <SelectValue placeholder={$_("settings.appearance.select_language")} />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="zh">中文 (简体)</SelectItem>
                                <SelectItem value="en">English</SelectItem>
                                <SelectItem value="ja">日本語</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                    
                    <Separator />
                    
                    <!-- 动画设置 -->
                    <div class="flex items-center justify-between">
                        <div>
                            <Label class="text-base font-medium">{$_("settings.appearance.animations")}</Label>
                            <p class="text-sm text-muted-foreground">{$_("settings.appearance.animations_desc")}</p>
                        </div>
                        <Switch checked={true} />
                    </div>
                    
                    <div class="flex items-center justify-between">
                        <div>
                            <Label class="text-base font-medium">{$_("settings.appearance.reduced_motion")}</Label>
                            <p class="text-sm text-muted-foreground">{$_("settings.appearance.reduced_motion_desc")}</p>
                        </div>
                        <Switch />
                    </div>
                </div>
            </NotionCard>
            
            <div class="flex justify-end">
                <Button>{$_("settings.save_changes")}</Button>
            </div>
        </div>
    </div>
</PageContent>

<style>
    /* 使用Inter字体确保符合Notion风格 */
    :global(label.text-base) {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
    }
    
    :global(p.text-sm) {
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        color: rgb(120, 119, 116);
    }
</style>
