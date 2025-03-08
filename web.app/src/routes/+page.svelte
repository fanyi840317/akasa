<script lang="ts">
    import { base } from "$app/paths";
    import { Button } from "$lib/components/ui/button";
    import { Badge } from "$lib/components/ui/badge";
    import { Clock, ArrowRight } from "lucide-svelte";
    import { onMount, onDestroy } from "svelte";
    import { _, locale } from 'svelte-i18n';
    import LanguageToggle from "$lib/components/language-toggle.svelte";

    const data = $props();

    // 设置目标日期（2025年4月1日）
    const targetDate = new Date('2025-04-01T00:00:00');
    
    // 使用 $state 声明确保响应式更新
    let days = $state('00');
    let hours = $state('00');
    let minutes = $state('00');
    let seconds = $state('00');

    let timer: ReturnType<typeof setInterval>;

    function updateCountdown() {
        const now = new Date();
        const difference = targetDate.getTime() - now.getTime();
        console.log('updateCountdown running, difference:', difference);

        if (difference <= 0) {
            // 如果已经到期
            days = '00';
            hours = '00';
            minutes = '00';
            seconds = '00';
            if (timer) clearInterval(timer);
            console.log('Countdown finished');
            return;
        }

        // 计算剩余时间
        days = Math.floor(difference / (1000 * 60 * 60 * 24)).toString().padStart(2, '0');
        hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)).toString().padStart(2, '0');
        minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60)).toString().padStart(2, '0');
        seconds = Math.floor((difference % (1000 * 60)) / 1000).toString().padStart(2, '0');
        console.log('Updated times:', { days, hours, minutes, seconds });
    }

    onMount(() => {
        console.log('onMount executed');
        // 立即执行一次
        updateCountdown();
        // 设置定时器，每秒更新一次
        timer = setInterval(updateCountdown, 1000);
        console.log('Timer set:', timer);
    });

    onDestroy(() => {
        console.log('onDestroy executed');
        // 清理定时器
        if (timer) {
            clearInterval(timer);
            console.log('Timer cleared');
        }
    });
</script>

<div class="min-h-screen bg-gradient-to-b from-background to-muted flex items-center justify-center relative overflow-hidden">
    <!-- 语言切换 -->
    <div class="absolute top-4 right-4 z-50">
        <LanguageToggle />
    </div>

    <!-- 背景装饰 -->
    <div class="absolute inset-0 bg-[radial-gradient(circle_at_50%_120%,rgba(120,119,198,0.3),rgba(0,0,0,0))]" />
    <div class="absolute inset-0 bg-grid-white/10" style="mask-image: radial-gradient(circle at 50% 50%, black, transparent);" />
    
    <div class="container mx-auto px-4 relative">
        <div class="max-w-2xl mx-auto text-center">
            <!-- 状态标签 -->
            <Badge variant="outline" class="mb-8 text-sm py-1 px-4">
                <Clock class="w-4 h-4 mr-2 animate-pulse" />
                {$_('common.comingSoon')}
            </Badge>

            <!-- 标题 -->
            <h1 class="text-4xl md:text-6xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-primary to-primary/50 tracking-wider">
                {$_('home.title')}
            </h1>

            <!-- 副标题 -->
            <p class="text-xl md:text-2xl text-muted-foreground mb-8 tracking-wide">
                {$_('home.subtitle')}
            </p>

            <!-- 预告文本 -->
            <p class="text-muted-foreground mb-12 max-w-xl mx-auto tracking-wide leading-relaxed">
                {$_('home.description')}
            </p>

            <!-- 联系按钮 -->
            <div class="flex justify-center">
                <Button size="lg" class="gap-2 tracking-widest" on:click={() => window.location.href = `mailto:x2.helsing@outlook.com?subject=${$_('home.emailSubject')}`}>
                    {$_('common.contactUs')}
                    <ArrowRight class="w-4 h-4" />
                </Button>
            </div>

            <!-- 倒计时 -->
            <div class="mt-16 grid grid-cols-2 sm:grid-cols-4 gap-4 max-w-md mx-auto">
                <div class="bg-card p-4 rounded-lg border">
                    <div class="text-2xl font-bold">{days}</div>
                    <div class="text-sm text-muted-foreground tracking-wider">{$_('common.days')}</div>
                </div>
                <div class="bg-card p-4 rounded-lg border">
                    <div class="text-2xl font-bold">{hours}</div>
                    <div class="text-sm text-muted-foreground tracking-wider">{$_('common.hours')}</div>
                </div>
                <div class="bg-card p-4 rounded-lg border">
                    <div class="text-2xl font-bold">{minutes}</div>
                    <div class="text-sm text-muted-foreground tracking-wider">{$_('common.minutes')}</div>
                </div>
                <div class="bg-card p-4 rounded-lg border">
                    <div class="text-2xl font-bold">{seconds}</div>
                    <div class="text-sm text-muted-foreground tracking-wider">{$_('common.seconds')}</div>
                </div>
            </div>
        </div>
    </div>

    <!-- 底部版权信息 -->
    <div class="absolute bottom-4 left-0 right-0 text-center text-sm text-muted-foreground">
        &copy; 2024 {$_('common.brand')}. All rights reserved.
    </div>
</div>

<style>
    .bg-grid-white\/10 {
        background-image: linear-gradient(to right, rgba(255,255,255,0.1) 1px, transparent 1px),
                         linear-gradient(to bottom, rgba(255,255,255,0.1) 1px, transparent 1px);
        background-size: 24px 24px;
    }
</style> 