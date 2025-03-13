<script lang="ts">
    import { Button } from "$lib/components/ui/button";
    import { Card, CardContent, CardHeader, CardTitle } from "$lib/components/ui/card";
    import { Construction } from "lucide-svelte";

    const title = "功能开发中";
    const description = "我们正在努力开发这项功能，敬请期待！";
</script>

<div class="container mx-auto p-16 flex items-center justify-center min-h-[calc(100vh-4rem)]">
    <Card class="w-full max-w-md text-center">
        <CardHeader>
            <div class="flex justify-center mb-4">
                <Construction class="h-12 w-12 text-primary animate-pulse" />
            </div>
            <CardTitle class="text-2xl font-bold">{title}</CardTitle>
        </CardHeader>
        <CardContent>
            <p class="text-muted-foreground mb-6">{description}</p>
            <div class="space-y-2">
                <div class="w-full bg-muted rounded-full h-2 overflow-hidden">
                    <div class="bg-primary h-full w-2/3 rounded-full animate-[progress_2s_ease-in-out_infinite]"></div>
                </div>
                <p class="text-sm text-muted-foreground">预计完成进度 66%</p>
            </div>
        </CardContent>
    </Card>
</div>

<style>
    @keyframes progress {
        0% { transform: translateX(-100%); }
        50% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
</style>