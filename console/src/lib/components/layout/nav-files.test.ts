import { render, screen, fireEvent } from '@testing-library/svelte';
import { describe, it, expect, vi } from 'vitest';
import NavFiles from './nav-files.svelte';

describe('NavFiles', () => {
	const mockChats = [
		{ id: 'chat1', name: 'First Chat', type: 'chat' as const },
		{ id: 'chat2', name: 'Second Chat', type: 'chat' as const },
		{ id: 'chat3', name: 'Third Chat', type: 'chat' as const }
	];

	it('renders chat list correctly', () => {
		render(NavFiles, {
			props: {
				chats: mockChats,
				selectedChatId: undefined,
				onChatClick: vi.fn(),
				onChatDelete: vi.fn(),
				onChatRename: vi.fn()
			}
		});

		expect(screen.getByText('First Chat')).toBeInTheDocument();
		expect(screen.getByText('Second Chat')).toBeInTheDocument();
		expect(screen.getByText('Third Chat')).toBeInTheDocument();
	});

	it('sets active state correctly based on selectedChatId', () => {
		const { rerender } = render(NavFiles, {
			props: {
				chats: mockChats,
				selectedChatId: 'chat2',
				onChatClick: vi.fn(),
				onChatDelete: vi.fn(),
				onChatRename: vi.fn()
			}
		});

		// 检查第二个聊天项是否被标记为激活状态
		const chatButtons = screen.getAllByRole('button');
		const secondChatButton = chatButtons.find(button => 
			button.textContent?.includes('Second Chat')
		);
		
		expect(secondChatButton).toHaveAttribute('data-state', 'active');
	});

	it('calls onChatClick when chat is clicked', async () => {
		const mockOnChatClick = vi.fn();
		
		render(NavFiles, {
			props: {
				chats: mockChats,
				selectedChatId: undefined,
				onChatClick: mockOnChatClick,
				onChatDelete: vi.fn(),
				onChatRename: vi.fn()
			}
		});

		const firstChatButton = screen.getByText('First Chat').closest('button');
		if (firstChatButton) {
			await fireEvent.click(firstChatButton);
		}

		expect(mockOnChatClick).toHaveBeenCalledWith('chat1');
	});

	it('updates active state when selectedChatId changes', () => {
		const { rerender } = render(NavFiles, {
			props: {
				chats: mockChats,
				selectedChatId: 'chat1',
				onChatClick: vi.fn(),
				onChatDelete: vi.fn(),
				onChatRename: vi.fn()
			}
		});

		// 更改选中的聊天ID
		rerender({
			chats: mockChats,
			selectedChatId: 'chat3',
			onChatClick: vi.fn(),
			onChatDelete: vi.fn(),
			onChatRename: vi.fn()
		});

		// 验证第三个聊天项现在是激活状态
		const chatButtons = screen.getAllByRole('button');
		const thirdChatButton = chatButtons.find(button => 
			button.textContent?.includes('Third Chat')
		);
		
		expect(thirdChatButton).toHaveAttribute('data-state', 'active');
	});

	it('handles empty chat list', () => {
		render(NavFiles, {
			props: {
				chats: [],
				selectedChatId: undefined,
				onChatClick: vi.fn(),
				onChatDelete: vi.fn(),
				onChatRename: vi.fn()
			}
		});

		// 应该没有聊天按钮
		const chatButtons = screen.queryAllByRole('button');
		expect(chatButtons).toHaveLength(0);
	});
});