<!-- svelte-ignore css_unused_selector -->

<script lang="ts">
	import { AffineEditorContainer, createEmptyDoc } from '@blocksuite/presets';
	import { signal } from '@preact/signals-core';
	import {
		ColorScheme,
		DocModeExtension,
		DocModeProvider,
		OverrideThemeExtension,
		SpecProvider,
		type DocMode,
		type ThemeExtension
	} from '@blocksuite/blocks';
	import { onMount, onDestroy } from 'svelte';

	import { Doc, Slot } from '@blocksuite/store'; // Added Doc
	import type { Disposable } from '@blocksuite/global/utils';
	import { createDocByJson, exportDocToJson } from './editor';

	// Import effects if they are not globally initialized elsewhere
	import { effects as blocksEffects } from '@blocksuite/blocks/effects';
	import { effects as presetsEffects } from '@blocksuite/presets/effects';

	import { cn } from '$lib/utils';
	let {
		initialJsonContent = undefined,
		class: className,
		readonly = $bindable(false)
	} = $props<{
		initialJsonContent?: string;
		class?: string;
		readonly?: boolean;
	}>();
	let editorContainer: HTMLDivElement;
	let editor: AffineEditorContainer;
	let resizeObserver: ResizeObserver | null = null;
	let styleCleanup: (() => void) | null = null;

	const createDocModeProvider = (editorInstance: AffineEditorContainer): DocModeProvider => {
		const DOC_MODE = 'edgeless'; // fixed to edgeless mode
		const doc_slots = new Map<string, Slot<DocMode>>();
		const service: DocModeProvider = {
			setPrimaryMode: (_mode: DocMode, doc_id: string): void => {
				doc_slots.get(doc_id)?.emit(DOC_MODE);
			},
			getPrimaryMode: (_doc_id: string): DocMode => {
				return DOC_MODE;
			},
			togglePrimaryMode: (_doc_id: string): DocMode => {
				return DOC_MODE;
			},
			onPrimaryModeChange: (handler: (mode: DocMode) => void, doc_id: string): Disposable => {
				if (!doc_slots.has(doc_id)) {
					doc_slots.set(doc_id, new Slot<DocMode>());
				}
				return doc_slots.get(doc_id)!.on(handler);
			},
			setEditorMode: (_mode: DocMode): void => {
				editorInstance.switchEditor(DOC_MODE);
			},
			getEditorMode: (): DocMode | null => editorInstance.mode
		};
		return service;
	};
	function removeTemporaryElements() {
		const toolbarWidget = document.querySelector('edgeless-toolbar-widget');
		if (!toolbarWidget) {
			return;
		}

		const templateButton = toolbarWidget.shadowRoot?.querySelector('edgeless-template-button');
		// const cover = document.createElement("edgeless-cover-tool-button");

		templateButton?.parentElement?.remove();
	}

	// CSS 隔离函数：动态管理 BlockSuite 的全局样式
	function setupStyleIsolation() {
		// 记录初始样式表数量
		const initialStyleSheetCount = document.styleSheets.length;
		
		// 创建 MutationObserver 监控 head 中的样式变化
		const styleObserver = new MutationObserver((mutations) => {
			mutations.forEach((mutation) => {
				if (mutation.type === 'childList') {
					mutation.addedNodes.forEach((node) => {
						if (node.nodeType === Node.ELEMENT_NODE) {
							const element = node as Element;
							// 只检查包含 input 元素选择器的样式
							if (element.tagName === 'STYLE') {
								const content = element.textContent || '';
								if (content.match(/input\s*[{:\[,]|input\s*$/m)) {
									// 为包含 input 的样式添加作用域限制
									try {
										scopeInputStyles(element);
										console.log("---scopeInputStyles---")

									} catch (e) {
										console.warn('Failed to scope input styles:', e);
									}
								}
							}
						}
					});
				}
			});
		});

		// 开始监控 document.head
		styleObserver.observe(document.head, {
			childList: true,
			subtree: true
		});

		// 在组件销毁时停止监控
		return () => {
			styleObserver.disconnect();
		};
	}

	// 为包含 input 的样式添加作用域限制
	function scopeInputStyles(styleElement: Element) {
		if (styleElement.tagName === 'STYLE') {
			const style = styleElement as HTMLStyleElement;
			let cssText = style.textContent || '';
			
			// 只处理包含 input 元素选择器的样式规则
			if (cssText.match(/input\s*[{:\[,]|input\s*$/m)) {
				// console.log(cssText);
				// 将 input 相关的全局样式限制在 .blocksuite-isolation-container 内
				cssText = cssText.replace(
					/(^|\}\s*)([^{}]*\binput\b[^{}]*\{[^{}]*\})/g,
					(match, prefix, rule) => {
						const selector = rule.split('{')[0].trim();
						const declarations = rule.split('{')[1];
						
						// 如果选择器包含完整的 input 单词，添加作用域前缀
						if (selector.match(/\binput\b/)) {
							const returnText = `${prefix}.blocksuite-isolation-container ${selector} {${declarations}`;
							// console.log("---scopeInputStyles---",returnText);

							return returnText;
						}
						return match;
					}
				);
				// console.log(cssText)
				style.textContent = cssText;
			}
		}
	}

	onMount(async () => {
		// 延迟初始化effects，只在编辑器实例创建前才注册
		// 这样可以最大程度减少对其他组件的影响
		
		const currentTheme = document.documentElement.dataset.theme;
		// const colorScheme = currentTheme === 'dark' ? ColorScheme.Dark : ColorScheme.Light;
		const colorScheme = ColorScheme.Dark;

		const themeExtension: ThemeExtension = {
			getAppTheme: () => signal(colorScheme),
			getEdgelessTheme: () => signal(colorScheme)
		};
		let doc: Doc | undefined = undefined;

		if (initialJsonContent) {
			try {
				const jsonData = initialJsonContent;
				doc = await createDocByJson(jsonData);

				if (!(doc instanceof Doc)) {
					console.error('createDocByJson did not return a Doc instance, falling back.');
					throw new Error('createDocByJson did not return a Doc instance');
				}
				// Assuming createDocByJson returns an initialized/loaded Doc.
				// If not, doc.load() or similar might be needed here.
			} catch (e) {
				console.error(
					'Failed to create document using createDocByJson or provided JSON is invalid:',
					e
				);
				// Fallback to an empty doc with the given ID
				doc = createEmptyDoc().init();
			}
		} else {
			// If no initial content, create a new empty doc
			doc = createEmptyDoc().init();
		}

		// 在 effects 初始化之前开始监控样式，因为 effects 会立即注入全局样式
		styleCleanup = setupStyleIsolation();
		
		// 只在编辑器实例创建前才注册effects，最小化对其他组件的影响
		if (!(window as any).__blocksuite_effects_initialized) {
			blocksEffects();
			presetsEffects();
			(window as any).__blocksuite_effects_initialized = true;
		}
		
		
		editor = new AffineEditorContainer();
		editor.doc = doc;
		editor.mode = 'edgeless';

		// 设置编辑器的只读模式
		if (readonly) {
			editor.doc.awarenessStore.setReadonly(doc.blockCollection, true);
		}

		const edgelessSpecs = SpecProvider.getInstance().getSpec('edgeless');
		edgelessSpecs.extend([
			OverrideThemeExtension(themeExtension),
			DocModeExtension(createDocModeProvider(editor))
		]);
		editor.edgelessSpecs = edgelessSpecs.value;

		// Example: Add a block to the surface
		// let surface = doc.getBlocksByFlavour("affine:surface")[0];
		// if (surface) {
		//   doc.addBlock(
		//     'affine:embed-github',
		//     {
		//       url: 'https://github.com/Milkdown/milkdown/pull/1215',
		//       xywh: '[500, 400, 752, 116]',
		//     },
		//     (surface as Block)?.id
		//   );
		// }

		editorContainer.appendChild(editor);
		await editor.updateComplete;
		// <div class="full-divider"></div>
		setTimeout(() => {
			removeTemporaryElements();
		}, 100);

		// 创建 ResizeObserver 监听容器大小变化
		resizeObserver = new ResizeObserver((entries) => {
			for (const entry of entries) {
				// 当容器大小变化时，延迟调用 removeTemporaryElements
				setTimeout(() => {
					removeTemporaryElements();
				}, 100);
			}
		});

		// 开始观察编辑器容器
		resizeObserver.observe(editorContainer);
	});

	// 监听readonly属性变化，动态切换编辑器的只读模式
	$effect(() => {
		if (editor && editor.doc) {
			editor.doc.awarenessStore.setReadonly(editor.doc.blockCollection, readonly);
		}
	});

	onDestroy(() => {
		// 清理样式监控器
		if (styleCleanup) {
			styleCleanup();
			styleCleanup = null;
		}
		
		// 清理 ResizeObserver
		if (resizeObserver) {
			resizeObserver.disconnect();
			resizeObserver = null;
		}
		
		// 清理编辑器实例
		if (editor) {
			try {
				editor.remove();
			} catch (e) {
				console.warn('Error disposing editor:', e);
			}
		}
		
		// 尝试清理可能影响其他组件的全局样式
		// try {
		// 	// 移除可能的全局样式污染
		// 	const styleSheets = document.styleSheets;
		// 	for (let i = 0; i < styleSheets.length; i++) {
		// 		const sheet = styleSheets[i];
		// 		if (sheet.href && (sheet.href.includes('blocksuite') || sheet.href.includes('affine'))) {
		// 			// 不直接删除，因为可能还有其他实例在使用
		// 			continue;
		// 		}
		// 	}
		// } catch (e) {
		// 	console.warn('Error cleaning up styles:', e);
		// }
	});
	export async function getContent() {
		return await exportDocToJson(editor.doc);
	}
</script>

<!-- CSS 隔离容器，防止 BlockSuite 样式泄露到其他组件 -->
<div class={cn('w-full h-full blocksuite-isolation-container', className)}>
	<div class="blocksuite-editor-wrapper" bind:this={editorContainer}></div>
</div>

<style>
	/* CSS 隔离：防止 BlockSuite 的全局样式影响其他组件 */
	.blocksuite-isolation-container {
		/* 创建新的层叠上下文和包含块 */
		isolation: isolate;
		contain: style layout;
		/* 重置可能被 BlockSuite 影响的样式 */
		all: initial;
		/* 恢复必要的布局样式 */
		display: block;
		width: 100%;
		height: 100%;
		box-sizing: border-box;
	}

	.blocksuite-editor-wrapper {
		width: 100%;
		height: 100%;
		position: relative;
		/* 确保编辑器容器有正确的显示属性 */
		display: block;
	}

</style>
