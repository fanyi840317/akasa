<script lang="ts">
    import { Separator } from "$lib/components/ui/separator";
    import { Avatar, AvatarFallback, AvatarImage } from "$lib/components/ui/avatar";
    import { Badge } from "$lib/components/ui/badge";
    import { onMount, onDestroy } from 'svelte';
    import { browser } from "$app/environment";
    import { writable } from "svelte/store";
    import { AffineEditorContainer } from '@blocksuite/presets';
    import { Doc, Schema, DocCollection } from '@blocksuite/store';
    import { AffineSchemas } from '@blocksuite/blocks';
    import '@blocksuite/presets/themes/affine.css';

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
            avatar: "https://github.com/shadcn.png"
        }
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
        const doc = collection.createDoc({ id: 'event-doc' });
        
        // 初始化文档结构
        await doc.load();
        const pageBlockId = doc.addBlock('affine:page', {});
        doc.addBlock('affine:surface', {}, pageBlockId);
        const noteId = doc.addBlock('affine:note', {}, pageBlockId);
        doc.addBlock('affine:paragraph', {}, noteId);

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
            titleInput.setSelectionRange(titleInput.value.length, titleInput.value.length);
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
            destroy: () => {}
        };
    };
</script>

<div class="space-y-6">
    <!-- 标题区域 -->
    <div class="px-6 pt-6 space-y-2">
        <input
            type="text"
            placeholder="无标题"
            class="text-4xl font-bold bg-transparent border-none outline-none w-full placeholder:text-muted-foreground/50 focus:ring-0"
            bind:value={eventTitle}
            use:autofocus
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
            <span class="text-sm text-muted-foreground">{creator.name}</span>
        </div>
        <div class="flex gap-2">
            <!-- 状态标签 -->
            <div class="flex items-center group hover:bg-gray-100 dark:hover:bg-gray-800 rounded p-1.5 cursor-pointer">
                <div class="flex items-center gap-2">
                    <span class="text-sm text-muted-foreground">状态</span>
                    <Badge variant="outline" class="text-xs">
                        <span class="mr-1.5 size-2 rounded-full bg-gray-400"></span>
                        {eventStatus}
                    </Badge>
                </div>
            </div>

            <!-- 位置输入 -->
            <div class="flex items-center group hover:bg-gray-100 dark:hover:bg-gray-800 rounded p-1.5 cursor-pointer">
                <div class="flex items-center gap-2">
                    <span class="text-sm text-muted-foreground">位置</span>
                    <input
                        type="text"
                        placeholder="添加位置"
                        class="text-sm bg-transparent border-none outline-none placeholder:text-muted-foreground/50 focus:ring-0 w-24"
                        bind:value={eventLocation}
                    />
                </div>
            </div>

            <!-- 日期选择器 -->
            <div class="flex items-center group hover:bg-gray-100 dark:hover:bg-gray-800 rounded p-1.5 cursor-pointer">
                <div class="flex items-center gap-2">
                    <span class="text-sm text-muted-foreground">日期</span>
                    <input
                        type="date"
                        class="text-sm bg-transparent border-none outline-none focus:ring-0"
                        bind:value={eventDate}
                    />
                </div>
            </div>
        </div>
    </div>

    <!-- 描述区域 -->
    <div class="px-6">
        <div 
            bind:this={editorContainer} 
            class="h-full w-full"
        />
    </div>
</div>