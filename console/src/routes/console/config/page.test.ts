import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/svelte';
import ConfigPage from './+page.svelte';
import { configStore } from '$lib/stores/config.svelte';

// Mock the config store
vi.mock('$lib/stores/config.svelte', () => ({
	configStore: {
		loadConfig: vi.fn(),
		updateConfig: vi.fn(),
		resetConfig: vi.fn(),
		validateConfig: vi.fn()
	}
}));

// Mock svelte-sonner
vi.mock('svelte-sonner', () => ({
	toast: {
		success: vi.fn(),
		error: vi.fn()
	}
}));

// Mock lucide-svelte icons
vi.mock('lucide-svelte', () => ({
	Settings: 'div',
	Save: 'div',
	RotateCcw: 'div',
	CheckCircle: 'div',
	AlertCircle: 'div'
}));

describe('Config Page', () => {
	beforeEach(() => {
		vi.clearAllMocks();
	});

	it('renders the config page with title', async () => {
		// Mock successful config load
		vi.mocked(configStore.loadConfig).mockResolvedValue({
			success: true,
			data: {
				system: { name: 'Test System' },
				components: {},
				llm: {}
			}
		});

		render(ConfigPage);

		expect(screen.getByText('系统配置')).toBeInTheDocument();
		expect(screen.getByText('验证配置')).toBeInTheDocument();
		expect(screen.getByText('重置')).toBeInTheDocument();
		expect(screen.getByText('保存配置')).toBeInTheDocument();
	});

	it('loads config on mount', async () => {
		vi.mocked(configStore.loadConfig).mockResolvedValue({
			success: true,
			data: {
				system: { name: 'Test System' },
				components: {},
				llm: {}
			}
		});

		render(ConfigPage);

		await waitFor(() => {
			expect(configStore.loadConfig).toHaveBeenCalledOnce();
		});
	});

	it('handles config load error', async () => {
		vi.mocked(configStore.loadConfig).mockResolvedValue({
			success: false,
			error: 'Failed to load config'
		});

		render(ConfigPage);

		await waitFor(() => {
			expect(configStore.loadConfig).toHaveBeenCalledOnce();
		});
	});

	it('saves config when save button is clicked', async () => {
		vi.mocked(configStore.loadConfig).mockResolvedValue({
			success: true,
			data: {
				system: { name: 'Test System' },
				components: {},
				llm: {}
			}
		});

		vi.mocked(configStore.updateConfig).mockResolvedValue({
			success: true,
			message: 'Config updated successfully'
		});

		render(ConfigPage);

		// Wait for initial load
		await waitFor(() => {
			expect(configStore.loadConfig).toHaveBeenCalledOnce();
		});

		// Click save button
		const saveButton = screen.getByText('保存配置');
		await fireEvent.click(saveButton);

		await waitFor(() => {
			expect(configStore.updateConfig).toHaveBeenCalledOnce();
		});
	});

	it('validates config when validate button is clicked', async () => {
		vi.mocked(configStore.loadConfig).mockResolvedValue({
			success: true,
			data: {
				system: { name: 'Test System' },
				components: {},
				llm: {}
			}
		});

		vi.mocked(configStore.validateConfig).mockResolvedValue({
			success: true,
			valid: true,
			results: [
				{ section: 'system', valid: true, message: 'Valid' }
			]
		});

		render(ConfigPage);

		// Wait for initial load
		await waitFor(() => {
			expect(configStore.loadConfig).toHaveBeenCalledOnce();
		});

		// Click validate button
		const validateButton = screen.getByText('验证配置');
		await fireEvent.click(validateButton);

		await waitFor(() => {
			expect(configStore.validateConfig).toHaveBeenCalledOnce();
		});
	});

	it('resets config when reset button is clicked and confirmed', async () => {
		// Mock window.confirm
		const confirmSpy = vi.spyOn(window, 'confirm').mockReturnValue(true);

		vi.mocked(configStore.loadConfig).mockResolvedValue({
			success: true,
			data: {
				system: { name: 'Test System' },
				components: {},
				llm: {}
			}
		});

		vi.mocked(configStore.resetConfig).mockResolvedValue({
			success: true,
			message: 'Config reset successfully'
		});

		render(ConfigPage);

		// Wait for initial load
		await waitFor(() => {
			expect(configStore.loadConfig).toHaveBeenCalledOnce();
		});

		// Click reset button
		const resetButton = screen.getByText('重置');
		await fireEvent.click(resetButton);

		expect(confirmSpy).toHaveBeenCalledWith('确定要重置配置到默认值吗？此操作不可撤销。');

		await waitFor(() => {
			expect(configStore.resetConfig).toHaveBeenCalledOnce();
		});

		confirmSpy.mockRestore();
	});

	it('does not reset config when reset is cancelled', async () => {
		// Mock window.confirm to return false
		const confirmSpy = vi.spyOn(window, 'confirm').mockReturnValue(false);

		vi.mocked(configStore.loadConfig).mockResolvedValue({
			success: true,
			data: {
				system: { name: 'Test System' },
				components: {},
				llm: {}
			}
		});

		render(ConfigPage);

		// Wait for initial load
		await waitFor(() => {
			expect(configStore.loadConfig).toHaveBeenCalledOnce();
		});

		// Click reset button
		const resetButton = screen.getByText('重置');
		await fireEvent.click(resetButton);

		expect(confirmSpy).toHaveBeenCalledWith('确定要重置配置到默认值吗？此操作不可撤销。');
		expect(configStore.resetConfig).not.toHaveBeenCalled();

		confirmSpy.mockRestore();
	});
});