<script lang="ts">
    import { Separator } from "$lib/components/ui/separator";
    import {
        Avatar,
        AvatarFallback,
        AvatarImage,
    } from "$lib/components/ui/avatar";
    import { Badge } from "$lib/components/ui/badge";
    import { ScrollArea } from "$lib/components/ui/scroll-area";
    import { Input } from "$lib/components/ui/input";
    import { onMount, onDestroy } from "svelte";
    import { browser } from "$app/environment";
    import { writable } from "svelte/store";
    import { AffineEditorContainer } from "@blocksuite/presets";
    import { Doc, Schema, DocCollection } from "@blocksuite/store";
    import { AffineSchemas } from "@blocksuite/blocks";
    import "@blocksuite/presets/themes/affine.css";

    // 组件属性类型定义
    interface Props {
        eventTitle?: string;
        eventLocation?: string;
        eventDate?: string;
        eventStatus?: string;
        creator?: {
            name: string;
            avatar: string;
        };
    }

    // 组件属性
    let {
        eventTitle = "",
        eventLocation = "",
        eventDate = "",
        eventStatus = "未开始",
        creator = {
            name: "范一",
            avatar: "https://github.com/shadcn.png",
        },
    }: Props = $props();

    let titleInput: HTMLInputElement;
    let editorContainer: HTMLDivElement;
    let editor: AffineEditorContainer;
    let collection: DocCollection;


    onMount(async () => {
        // 初始化编辑器
        const schema = new Schema().register(AffineSchemas);
        collection = new DocCollection({ schema });
        collection.meta.initialize();

        // 创建文档
        const doc = collection.createDoc({ id: "event-doc" });

        // 初始化文档结构
        await doc.load();
        const pageBlockId = doc.addBlock("affine:page", {});
        // doc.addBlock('affine:surface', {}, pageBlockId);
        const noteId = doc.addBlock("affine:note", {}, pageBlockId);
        doc.addBlock("affine:paragraph", {}, noteId);

        // 创建编辑器实例
        editor = new AffineEditorContainer();
        editor.doc = doc;

        // 配置编辑器
        editor.slots.docLinkClicked.on(({ docId }) => {
            const target = collection.getDoc(docId) as Doc;
            editor.doc = target;
        });

        // 将编辑器挂载到容器
        if (editorContainer && editor) {
            editorContainer.appendChild(editor as unknown as Node);
        }

        // 自动聚焦到标题输入框
        if (titleInput && !eventTitle) {
            titleInput.focus();
            titleInput.setSelectionRange(
                titleInput.value.length,
                titleInput.value.length,
            );
        }
    });

    onDestroy(() => {
        if (editor) {
            editor.remove?.();
        }
        if (collection) {
            (collection as any).dispose?.();
        }
    });

    // 自动聚焦函数
    const autofocus = (node: HTMLInputElement) => {
        titleInput = node;
        return {
            destroy: () => {},
        };
    };
</script>

<ScrollArea class="h-[calc(100vh-4rem)]">
    <div class="space-y-6">
        <!-- 标题区域 -->
        <div class="px-6 pt-6 space-y-2">
            <Input
                type="text"
                placeholder="无标题"
                class="text-4xl font-bold bg-transparent border-none outline-none w-full placeholder:text-muted-foreground/50 focus:ring-0"
                bind:value={eventTitle}
            />
            <Separator class="my-4" />
        </div>

        <!-- 属性区域 -->
        <div class="px-6 space-y-4">
            <div class="flex gap-2">
                <span class="text-sm text-muted-foreground">创作者</span>
                <Avatar class="h-6 w-6">
                    <AvatarImage src={creator.avatar} alt={creator.name} />
                    <AvatarFallback>{creator.name[0]}</AvatarFallback>
                </Avatar>
                <span class="text-sm text-muted-foreground">{creator.name}</span
                >
            </div>
            <div class="flex gap-4">
                <!-- 状态标签 -->
                <div
                    class="flex flex-col group hover:bg-gray-100 dark:hover:bg-gray-800 rounded p-1.5 cursor-pointer"
                >
                    <span class="text-sm text-muted-foreground mb-1">状态</span>
                    <Badge variant="outline" class="text-xs">
                        <span class="mr-1.5 size-2 rounded-full bg-gray-400"
                        ></span>
                        {eventStatus}
                    </Badge>
                </div>

                <!-- 位置输入 -->
                <div
                    class="flex flex-col group hover:bg-gray-100 dark:hover:bg-gray-800 rounded p-1.5 cursor-pointer"
                >
                    <span class="text-sm text-muted-foreground mb-1">位置</span>
                    <Input
                        type="text"
                        placeholder="添加位置"
                        class="text-sm bg-transparent border-none outline-none placeholder:text-muted-foreground/50 focus:ring-0 w-24"
                        bind:value={eventLocation}
                    />
                </div>

                <!-- 日期选择器 -->
                <div
                    class="flex flex-col group hover:bg-gray-100 dark:hover:bg-gray-800 rounded p-1.5 cursor-pointer"
                >
                    <span class="text-sm text-muted-foreground mb-1">日期</span>
                    <Input
                        type="date"
                        class="text-sm bg-transparent border-none outline-none focus:ring-0"
                        bind:value={eventDate}
                    />
                </div>
            </div>
        </div>

        <!-- 描述区域 -->
        <div class="px-6">
            <div bind:this={editorContainer} class="h-full w-full" />
        </div>
    </div>
</ScrollArea>

<style>
    :root {
        --affine-theme-mode: dark;

        --affine-popover-shadow: 0px 1px 10px -6px rgba(24, 39, 75, 0.08),
            0px 3px 16px -6px rgba(24, 39, 75, 0.04);
        --affine-font-h-1: 28px;
        --affine-font-h-2: 26px;
        --affine-font-h-3: 24px;
        --affine-font-h-4: 22px;
        --affine-font-h-5: 20px;
        --affine-font-h-6: 18px;
        --affine-font-base: 16px;
        --affine-font-sm: 14px;
        --affine-font-xs: 12px;
        --affine-line-height: calc(1em + 8px);
        --affine-z-index-modal: 1000;
        --affine-z-index-popover: 1000;
        --affine-font-family: Avenir Next, Poppins, apple-system,
            BlinkMacSystemFont, Helvetica Neue, Tahoma, PingFang SC,
            Microsoft Yahei, Arial, Hiragino Sans GB, sans-serif,
            Apple Color Emoji, Segoe UI Emoji, Segoe UI Symbol, Noto Color Emoji;
        --affine-font-number-family: Roboto Mono, apple-system,
            BlinkMacSystemFont, Helvetica Neue, Tahoma, PingFang SC,
            Microsoft Yahei, Arial, Hiragino Sans GB, sans-serif,
            Apple Color Emoji, Segoe UI Emoji, Segoe UI Symbol, Noto Color Emoji;
        --affine-font-code-family: Space Mono, Consolas, Menlo, Monaco, Courier,
            monospace, apple-system, BlinkMacSystemFont, Helvetica Neue, Tahoma,
            PingFang SC, Microsoft Yahei, Arial, Hiragino Sans GB, sans-serif,
            Apple Color Emoji, Segoe UI Emoji, Segoe UI Symbol, Noto Color Emoji;
        --affine-paragraph-space: 8px;
        --affine-popover-radius: 10px;
        --affine-zoom: 1;
        --affine-scale: calc(1 / var(--affine-zoom));

        --affine-brand-color: rgb(84, 56, 255);
        --affine-primary-color: rgb(118, 95, 254);
        --affine-secondary-color: rgb(144, 150, 245);
        --affine-tertiary-color: rgb(30, 30, 30);
        --affine-hover-color: rgba(255, 255, 255, 0.1);
        --affine-icon-color: rgb(168, 168, 160);
        --affine-border-color: rgb(57, 57, 57);
        --affine-divider-color: rgb(114, 114, 114);
        --affine-placeholder-color: rgb(62, 62, 63);
        --affine-quote-color: rgb(100, 95, 130);
        --affine-link-color: rgb(185, 191, 227);
        --affine-edgeless-grid-color: rgb(49, 49, 49);
        --affine-success-color: rgb(77, 213, 181);
        --affine-warning-color: rgb(255, 123, 77);
        --affine-error-color: rgb(212, 140, 130);
        --affine-processing-color: rgb(195, 215, 255);
        --affine-text-emphasis-color: rgb(208, 205, 220);
        --affine-text-primary-color: rgb(234, 234, 234);
        --affine-text-secondary-color: rgb(156, 156, 160);
        --affine-text-disable-color: rgb(119, 117, 125);
        --affine-black-10: rgba(255, 255, 255, 0.1);
        --affine-black-30: rgba(255, 255, 255, 0.3);
        --affine-black-50: rgba(255, 255, 255, 0.5);
        --affine-black-60: rgba(255, 255, 255, 0.6);
        --affine-black-80: rgba(255, 255, 255, 0.8);
        --affine-black-90: rgba(255, 255, 255, 0.9);
        --affine-black: rgb(255, 255, 255);
        --affine-white-10: rgba(0, 0, 0, 0.1);
        --affine-white-30: rgba(0, 0, 0, 0.3);
        --affine-white-50: rgba(0, 0, 0, 0.5);
        --affine-white-60: rgba(0, 0, 0, 0.6);
        --affine-white-80: rgba(0, 0, 0, 0.8);
        --affine-white-90: rgba(0, 0, 0, 0.9);
        --affine-white: rgb(0, 0, 0);
        --affine-background-code-block: rgb(41, 44, 51);
        --affine-background-tertiary-color: rgb(30, 30, 30);
        --affine-background-processing-color: rgb(255, 255, 255);
        --affine-background-error-color: rgb(255, 255, 255);
        --affine-background-warning-color: rgb(255, 255, 255);
        --affine-background-success-color: rgb(255, 255, 255);
        --affine-background-primary-color: rgb(20, 20, 20);
        --affine-background-hover-color: rgb(47, 47, 47);
        --affine-background-secondary-color: rgb(32, 32, 32);
        --affine-background-modal-color: rgba(0, 0, 0, 0.8);
        --affine-background-overlay-panel-color: rgb(30, 30, 30);
        --affine-tag-blue: rgb(10, 84, 170);
        --affine-tag-green: rgb(55, 135, 79);
        --affine-tag-teal: rgb(33, 145, 138);
        --affine-tag-white: rgb(84, 84, 84);
        --affine-tag-purple: rgb(59, 38, 141);
        --affine-tag-red: rgb(139, 63, 63);
        --affine-tag-pink: rgb(194, 132, 132);
        --affine-tag-yellow: rgb(187, 165, 61);
        --affine-tag-orange: rgb(231, 161, 58);
        --affine-tag-gray: rgb(41, 41, 41);
        --affine-palette-yellow: rgb(255, 232, 56);
        --affine-palette-orange: rgb(255, 175, 56);
        --affine-palette-tangerine: rgb(255, 99, 31);
        --affine-palette-red: rgb(252, 63, 85);
        --affine-palette-magenta: rgb(255, 56, 179);
        --affine-palette-purple: rgb(182, 56, 255);
        --affine-palette-navy: rgb(59, 37, 204);
        --affine-palette-blue: rgb(79, 144, 255);
        --affine-palette-green: rgb(16, 203, 134);
        --affine-palette-grey: rgb(153, 153, 153);
        --affine-palette-white: rgb(255, 255, 255);
        --affine-palette-black: rgb(0, 0, 0);
    }
    .embed-card-modal-mask {
        position: absolute;
        left: 0;
        right: 0;
        top: 0;
        bottom: 0;
        margin: auto;
        z-index: 10001;
    }

    .embed-card-modal-wrapper {
        flex-direction: column;
        position: absolute;
        left: 0;
        right: 0;
        top: 0;
        bottom: 0;
        margin: auto;
        z-index: 10002;
        width: 305px;
        height: max-content;
        padding: 12px;
        gap: 12px;
        border-radius: 8px;
        font-size: var(--affine-font-xs);
        line-height: 20px;
    }
</style>
