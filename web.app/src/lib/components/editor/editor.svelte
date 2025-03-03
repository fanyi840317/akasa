<script lang="ts">
	import './styles/prosemirror.css';

	import { getPrevText } from './editor.js';
	import { createLocalStorageStore } from '$lib/stores/localStorage.js';
	import { createDebouncedCallback, noop } from '$lib/utils.js';
	import { Editor, Extension, type JSONContent } from '@tiptap/core';
	import type { EditorProps } from '@tiptap/pm/view';
	import { useCompletion } from 'ai/react';
	import ImageResizer from './extensions/ImageResizer.svelte';
	import { onMount, createEventDispatcher } from 'svelte';
	import { defaultEditorContent } from './default-content.ts';
	import { defaultExtensions } from './extensions/index.js';
	import { defaultEditorProps } from './props.ts';
	import { toast } from 'svelte-sonner';

	import EditorBubbleMenu from './bubble-menu/index.svelte';

	const dispatch = createEventDispatcher();

	/**
	 * The API route to use for the OpenAI completion API.
	 * Defaults to "/api/generate".
	 */
	export let completionApi = '/api/generate';
	/**
	 * Additional classes to add to the editor container.
	 */
	let className =
		'notion-editor-container relative w-full p-1 focus-within:ring-0 focus-within:ring-offset-0';
	export { className as class };
	/**
	 * The default value to use for the editor.
	 * Defaults to defaultEditorContent.
	 */
	export let defaultValue: JSONContent | string = defaultEditorContent;
	/**
	 * A list of extensions to use for the editor, in addition to the default Novel extensions.
	 * Defaults to [].
	 */
	export let extensions: Extension[] = [];
	/**
	 * Props to pass to the underlying Tiptap editor, in addition to the default Novel editor props.
	 * Defaults to {}.
	 */
	export let editorProps: EditorProps = {};
	/**
	 * A callback function that is called whenever the editor is updated.
	 * Defaults to () => {}.
	 */
	export let onUpdate: (editor?: Editor) => void | Promise<void> = noop;
	/**
	 * A callback function that is called whenever the editor is updated, but only after the defined debounce duration.
	 * Defaults to () => {}.
	 */
	export let onDebouncedUpdate: (editor?: Editor) => void | Promise<void> = noop;
	/**
	 * The duration (in milliseconds) to debounce the onDebouncedUpdate callback.
	 * Defaults to 750.
	 */
	export let debounceDuration = 750;
	/**
	 * The key to use for storing the editor's value in local storage.
	 * Defaults to "novel__content".
	 */
	export let storageKey = 'novel__content';
	/**
	 * Disable local storage read/save.
	 * @default false
	 */
	export let disableLocalStorage = false;
 
	export let editor: Editor | undefined = undefined;

	let element: Element;
	const isLoading = false;
	
	// Modified editor props to handle focus and blur
	const editorFocusProps = {
		handleDOMEvents: {
			focus: (view, event) => {
				dispatch('focus', { event });
				return false; // Let the default handler run
			},
			blur: (view, event) => {
				dispatch('blur', { event });
				return false; // Let the default handler run
			},
			...editorProps.handleDOMEvents
		},
		...editorProps
	};

	const content = createLocalStorageStore(storageKey, defaultValue);
	let hydrated = false;
	$: if (editor && !hydrated) {
		const value = disableLocalStorage ? defaultValue : $content;

		if (value) {
			editor.commands.setContent(value);
		}

		hydrated = true;
	}

	let prev = '';

	const debouncedUpdates = createDebouncedCallback(async ({ editor }) => {
		if (!disableLocalStorage) {
			const json = editor.getJSON();
			content.set(json);
		}

		onDebouncedUpdate(editor);
	}, debounceDuration);

	onMount(() => {
		editor = new Editor({
			element: element,
			onTransaction: () => {
				// force re-render so `editor.isActive` works as expected
				editor = editor;
			},
			extensions: [...defaultExtensions, ...extensions],
			editorProps: {
				...defaultEditorProps,
				...editorFocusProps
			},
			onUpdate: (e) => {
				const selection = e.editor.state.selection;
				const lastTwo = getPrevText(e.editor, {
					chars: 2
				});

				if (lastTwo === '++' && !isLoading) {
					e.editor.commands.deleteRange({
						from: selection.from - 2,
						to: selection.from
					});
				} else {
					onUpdate(e.editor);
					debouncedUpdates(e);
				}
			},
			autofocus: false // Changed to false for better UX
		});

		return () => {
			if (editor) {
				editor.destroy();
			}
		};
	});
</script>

{#if editor && editor.isEditable}
	<EditorBubbleMenu {editor} />
{/if}

<div id="editor" class={className} bind:this={element}>
	<slot />
	{#if editor?.isActive('image')}
		<ImageResizer {editor} />
	{/if}
</div>

<style>
	/* Notion-like styling for editor container */
	:global(.notion-editor-container) {
		font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, "Apple Color Emoji", Arial, sans-serif, "Segoe UI Emoji", "Segoe UI Symbol";
		color: rgb(55, 53, 47);
	}
	
	:global(.notion-editor-container:focus-within) {
		background-color: transparent;
	}
	
	:global(.notion-editor-container .ProseMirror) {
		padding: 0;
		min-height: 150px;
		outline: none !important;
	}
	
	:global(.notion-editor-container .ProseMirror:focus) {
		outline: none !important;
	}
</style>
