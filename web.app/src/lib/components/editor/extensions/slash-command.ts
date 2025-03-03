import { Editor, Extension, type Range } from '@tiptap/core';
import Suggestion from '@tiptap/suggestion';

import tippy from 'tippy.js';

import {
	CheckSquare,
	Code,
	Heading1,
	Heading2,
	Heading3,
	List,
	ListOrdered,
	MessageSquarePlus,
	Text,
	TextQuote,
	Wand2
} from 'lucide-svelte';
import CommandList from './CommandList.svelte';
// import { toast } from 'sonner';
// import va from '@vercel/analytics';
// import { startImageUpload } from '@/ui/editor/plugins/upload-images';
import type { SvelteComponent } from 'svelte';

export interface CommandItemProps {
	title: string;
	description: string;
	icon: SvelteComponent;
}

interface CommandProps {
	editor: Editor;
	range: Range;
}

// Safe range validation and deletion
const safelyDeleteRange = (editor: Editor, range: Range) => {
	try {
		// Validate the range
		const doc = editor.state.doc;
		const validFrom = Math.max(0, Math.min(range.from, doc.content.size));
		const validTo = Math.max(0, Math.min(range.to, doc.content.size));
		
		// Create valid range
		const validRange = { from: validFrom, to: validTo };
		
		// Only attempt to delete if range is valid and non-empty
		if (validFrom < validTo) {
			return editor.chain().focus().deleteRange(validRange);
		}
		
		// If range is invalid or empty, just return the chain without deleting
		return editor.chain().focus();
	} catch (err) {
		console.error('Error in safelyDeleteRange:', err);
		// Return a chain that will at least not crash
		return editor.chain().focus();
	}
};

// Helper to check if we're at the document start
const isAtDocumentStart = (range: Range) => {
	return range.from === 0;
};

// Function to safely set a heading node
const safelySetHeading = (editor: Editor, range: Range, level: number) => {
	try {
		// First ensure we delete the range safely
		const chain = safelyDeleteRange(editor, range);
		
		// If at document start, insert a paragraph first if needed
		if (isAtDocumentStart(range)) {
			if (editor.isEmpty) {
				return chain.setNode('heading', { level }).run();
			} else {
				// Ensure there's proper node structure
				return chain.setNode('heading', { level }).run();
			}
		}
		
		// Otherwise ensure we set the heading properly
		return chain.setNode('heading', { level }).run();
	} catch (err) {
		console.error('Error in safelySetHeading:', err);
		// Fallback to basic paragraph
		return editor.chain().focus().setParagraph().run();
	}
};

// Function to safely set a paragraph
const safelySetParagraph = (editor: Editor, range: Range) => {
	try {
		// Delete range first
		const chain = safelyDeleteRange(editor, range);
		
		// If at document start, handle differently
		if (isAtDocumentStart(range)) {
			if (editor.isEmpty) {
				return chain.setParagraph().run();
			}
		}
		
		return chain.setParagraph().run();
	} catch (err) {
		console.error('Error in safelySetParagraph:', err);
		return editor.chain().focus().run();
	}
};

// Function to safely toggle a list
const safelyToggleList = (editor: Editor, range: Range, listType: 'bulletList' | 'orderedList' | 'taskList') => {
	try {
		// Delete range first
		const chain = safelyDeleteRange(editor, range);
		
		// If at document start with empty editor, ensure we have content structure
		if (isAtDocumentStart(range) && editor.isEmpty) {
			chain.setParagraph();
		}
		
		// Toggle the appropriate list type
		if (listType === 'bulletList') {
			return chain.toggleBulletList().run();
		} else if (listType === 'orderedList') {
			return chain.toggleOrderedList().run();
		} else if (listType === 'taskList') {
			return chain.toggleTaskList().run();
		}
	} catch (err) {
		console.error(`Error in safelyToggleList (${listType}):`, err);
		return editor.chain().focus().setParagraph().run();
	}
};

// Function to safely toggle a block
const safelyToggleBlock = (editor: Editor, range: Range, blockType: 'blockquote' | 'codeBlock') => {
	try {
		// Delete range first
		const chain = safelyDeleteRange(editor, range);
		
		// If at document start with empty editor, ensure we have content structure
		if (isAtDocumentStart(range) && editor.isEmpty) {
			chain.setParagraph();
		}
		
		// Toggle the appropriate block type
		if (blockType === 'blockquote') {
			return chain.toggleBlockquote().run();
		} else if (blockType === 'codeBlock') {
			return chain.toggleCodeBlock().run();
		}
	} catch (err) {
		console.error(`Error in safelyToggleBlock (${blockType}):`, err);
		return editor.chain().focus().setParagraph().run();
	}
};

const Command = Extension.create({
	name: 'slash-command',
	addOptions() {
		return {
			suggestion: {
				char: '/',
				command: ({ editor, range, props }: { editor: Editor; range: Range; props: any }) => {
					props.command({ editor, range });
				}
			}
		};
	},
	addProseMirrorPlugins() {
		return [
			Suggestion({
				editor: this.editor,
				...this.options.suggestion
			})
		];
	}
});

const getSuggestionItems = ({ query }: { query: string }) => {
	return [
		{
			title: 'Continue writing',
			description: 'Use AI to expand your thoughts.',
			searchTerms: ['gpt'],
			icon: Wand2
		},
		{
			title: 'Text',
			description: 'Just start typing with plain text.',
			searchTerms: ['p', 'paragraph'],
			icon: Text,
			command: ({ editor, range }: CommandProps) => {
				safelySetParagraph(editor, range);
			}
		},
		{
			title: 'To-do List',
			description: 'Track tasks with a to-do list.',
			searchTerms: ['todo', 'task', 'list', 'check', 'checkbox'],
			icon: CheckSquare,
			command: ({ editor, range }: CommandProps) => {
				safelyToggleList(editor, range, 'taskList');
			}
		},
		{
			title: 'Heading 1',
			description: 'Big section heading.',
			searchTerms: ['title', 'big', 'large'],
			icon: Heading1,
			command: ({ editor, range }: CommandProps) => {
				safelySetHeading(editor, range, 1);
			}
		},
		{
			title: 'Heading 2',
			description: 'Medium section heading.',
			searchTerms: ['subtitle', 'medium'],
			icon: Heading2,
			command: ({ editor, range }: CommandProps) => {
				safelySetHeading(editor, range, 2);
			}
		},
		{
			title: 'Heading 3',
			description: 'Small section heading.',
			searchTerms: ['subtitle', 'small'],
			icon: Heading3,
			command: ({ editor, range }: CommandProps) => {
				safelySetHeading(editor, range, 3);
			}
		},
		{
			title: 'Bullet List',
			description: 'Create a simple bullet list.',
			searchTerms: ['unordered', 'point'],
			icon: List,
			command: ({ editor, range }: CommandProps) => {
				safelyToggleList(editor, range, 'bulletList');
			}
		},
		{
			title: 'Numbered List',
			description: 'Create a numbered list.',
			searchTerms: ['ordered'],
			icon: ListOrdered,
			command: ({ editor, range }: CommandProps) => {
				safelyToggleList(editor, range, 'orderedList');
			}
		},
		{
			title: 'Quote',
			description: 'Capture a quote.',
			searchTerms: ['blockquote'],
			icon: TextQuote,
			command: ({ editor, range }: CommandProps) => {
				safelyToggleBlock(editor, range, 'blockquote');
			}
		},
		{
			title: 'Code',
			description: 'Add a code block.',
			searchTerms: ['codeblock'],
			icon: Code,
			command: ({ editor, range }: CommandProps) => {
				safelyToggleBlock(editor, range, 'codeBlock');
			}
		}
	].filter((item) => {
		if (typeof query === 'string' && query.length > 0) {
			const search = query.toLowerCase();
			return (
				item.title.toLowerCase().includes(search) ||
				item.description.toLowerCase().includes(search) ||
				(item.searchTerms && item.searchTerms.some((term: string) => term.includes(search)))
			);
		}
		return true;
	});
};

export const updateScrollView = (container: HTMLElement, item: HTMLElement) => {
	const containerHeight = container.offsetHeight;
	const itemHeight = item ? item.offsetHeight : 0;

	const top = item.offsetTop;
	const bottom = top + itemHeight;

	if (top < container.scrollTop) {
		container.scrollTop = top;
	} else if (bottom > containerHeight + container.scrollTop) {
		container.scrollTop = bottom - containerHeight;
	}
};

const renderItems = () => {
	let component: any;
	let popup: any;

	return {
		onStart: (props: { editor: Editor; clientRect: DOMRect }) => {
			// Create a container element for the component
			const container = document.createElement('div');
			document.body.appendChild(container);
			
			component = new CommandList({
				target: container,
				props: {
					editor: props.editor,
					range: props.editor.state.selection,
					items: getSuggestionItems({ query: '' })
				}
			});

			// @ts-ignore
			popup = tippy('body', {
				getReferenceClientRect: props.clientRect,
				appendTo: () => document.body,
				content: container,
				showOnCreate: true,
				interactive: true,
				trigger: 'manual',
				placement: 'bottom-start',
				onDestroy: () => {
					container.remove(); // Clean up the container when tippy is destroyed
				}
			});
		},
		onUpdate: (props: { editor: Editor; clientRect: DOMRect; query: string }) => {
			component.$set({
				items: getSuggestionItems({ query: props.query }),
				editor: props.editor,
				range: props.editor.state.selection
			});

			popup[0].setProps({
				getReferenceClientRect: props.clientRect
			});
		},
		onKeyDown: (props: { event: KeyboardEvent }) => {
			if (props.event.key === 'Escape') {
				popup[0].hide();
				return true;
			}

			// Handle keyboard events directly instead of trying to access component.onKeyDown
			const navigationKeys = ['ArrowUp', 'ArrowDown', 'Enter'];
			
			if (navigationKeys.includes(props.event.key)) {
				props.event.preventDefault();
				
				// For Enter, select the currently highlighted item
				if (props.event.key === 'Enter') {
					// Dispatch a custom event to the component to select the current item
					const customEvent = new CustomEvent('select-current-item');
					component.$$.root?.dispatchEvent(customEvent);
					return true;
				}
				
				// Update component for navigation
				component.$set({
					navigationKey: props.event.key
				});
				
				return true;
			}
			
			return false;
		},
		onExit: () => {
			popup[0].destroy();
			// @ts-ignore
			component.$destroy();
		}
	};
};

const SlashCommand = Command.configure({
	suggestion: {
		items: getSuggestionItems,
		render: renderItems
	}
});

export default SlashCommand;
