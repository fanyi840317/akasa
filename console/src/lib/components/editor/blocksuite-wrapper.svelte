<script lang="ts">
	import { onMount, createEventDispatcher } from 'svelte';
	import { mount } from 'svelte';
	import BlocksuiteEditor from './blocksuite-editor.svelte';

	let container: HTMLDivElement;
	let shadowRoot: ShadowRoot;
	let editorInstance: any;
	let unmountEditor: (() => void) | undefined;

	// 接收与 BlocksuiteEditor 相同的属性
	let { initialJsonContent = undefined, readonly = false, class: className = '' } = $props<{
		initialJsonContent?: string;
		class?: string;
		readonly?: boolean;
	}>();

	onMount(() => {
		// 创建 Shadow DOM
		shadowRoot = container.attachShadow({ mode: 'open' });

		// 创建一个容器元素
		const editorContainer = document.createElement('div');
		editorContainer.style.width = '100%';
		editorContainer.style.height = '100%';
		shadowRoot.appendChild(editorContainer);

		// 使用 Svelte 5 的 mount 函数创建组件
		editorInstance = mount(BlocksuiteEditor, {
			target: editorContainer,
			props: {
				initialJsonContent,
				readonly,
				class: 'w-full h-full'
			}
		});

		// 保存 unmount 函数以便清理
		unmountEditor = () => {
			if (editorInstance && typeof editorInstance.$destroy === 'function') {
				editorInstance.$destroy();
			}
		};

		return () => {
			if (unmountEditor) {
				unmountEditor();
			}
		};
	});

	// 导出 getContent 方法，以便外部可以调用
	export async function getContent() {
		if (editorInstance && typeof editorInstance.getContent === 'function') {
			return await editorInstance.getContent();
		}
		return null;
	}
</script>

<div bind:this={container} class={className}></div>