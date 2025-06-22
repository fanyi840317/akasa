import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { configStore } from './config.svelte';

// Mock fetch globally
const mockFetch = vi.fn() as unknown as typeof fetch;
global.fetch = mockFetch;

describe('ConfigStore', () => {
	beforeEach(() => {
		vi.clearAllMocks();
	});

	afterEach(() => {
		vi.resetAllMocks();
	});

	describe('loadConfig', () => {
		it('successfully loads configuration', async () => {
			const mockResponse: { success: boolean; data: Record<string, unknown> } = {
			success: true,
			data: {
				system: { name: 'Test System' },
				components: {},
				llm: {}
			}
		};

			mockFetch.mockResolvedValueOnce({
			ok: true,
			json: () => Promise.resolve(mockResponse)
		} as Response);

			const result = await configStore.loadConfig();

			expect(mockFetch).toHaveBeenCalledWith('http://localhost:8000/api/config/');
			expect(result).toEqual(mockResponse);
		});

		it('handles HTTP error responses', async () => {
			const errorResponse = {
				success: false,
				error: 'Configuration not found'
			};

			mockFetch.mockResolvedValueOnce({
				ok: false,
				status: 404,
				json: () => Promise.resolve(errorResponse)
			});

			const result = await configStore.loadConfig();

			expect(result).toEqual({
				success: false,
				error: 'Configuration not found'
			});
		});

		it('handles network errors', async () => {
			mockFetch.mockRejectedValueOnce(new Error('Network error'));

			const result = await configStore.loadConfig();

			expect(result).toEqual({
				success: false,
				error: 'Network error'
			});
		});
	});

	describe('loadSystemConfig', () => {
		it('successfully loads system configuration', async () => {
			const mockResponse = {
				success: true,
				data: { name: 'Test System', version: '1.0.0' }
			};

			mockFetch.mockResolvedValueOnce({
				ok: true,
				json: () => Promise.resolve(mockResponse)
			});

			const result = await configStore.loadSystemConfig();

			expect(mockFetch).toHaveBeenCalledWith('http://localhost:8000/api/config/system');
			expect(result).toEqual(mockResponse);
		});
	});

	describe('loadComponentsConfig', () => {
		it('successfully loads components configuration', async () => {
			const mockResponse: { success: boolean; data: Record<string, unknown> } = {
			success: true,
			data: { search: { enabled: true } }
		};

			mockFetch.mockResolvedValueOnce({
				ok: true,
				json: () => Promise.resolve(mockResponse)
			});

			const result = await configStore.loadComponentsConfig();

			expect(mockFetch).toHaveBeenCalledWith('http://localhost:8000/api/config/components');
			expect(result).toEqual(mockResponse);
		});
	});

	describe('loadLLMConfig', () => {
		it('successfully loads LLM configuration', async () => {
			const mockResponse: { success: boolean; data: Record<string, unknown> } = {
			success: true,
			data: { openai: { api_key: 'sk-test' } }
		};

			mockFetch.mockResolvedValueOnce({
				ok: true,
				json: () => Promise.resolve(mockResponse)
			});

			const result = await configStore.loadLLMConfig();

			expect(mockFetch).toHaveBeenCalledWith('http://localhost:8000/api/config/llm');
			expect(result).toEqual(mockResponse);
		});
	});

	describe('loadRawConfig', () => {
		it('successfully loads raw configuration', async () => {
			const mockResponse: { success: boolean; data: Record<string, unknown> } = {
			success: true,
			data: {
				default: { system: { name: 'Default' } },
				user: { system: { name: 'User Override' } },
				merged: { system: { name: 'User Override' } }
			}
		};

			mockFetch.mockResolvedValueOnce({
				ok: true,
				json: () => Promise.resolve(mockResponse)
			});

			const result = await configStore.loadRawConfig();

			expect(mockFetch).toHaveBeenCalledWith('http://localhost:8000/api/config/raw');
			expect(result).toEqual(mockResponse);
		});
	});

	describe('updateConfig', () => {
		it('successfully updates configuration', async () => {
			const configData = {
				system: { name: 'Updated System' }
			};

			const mockResponse: { success: boolean; message: string } = {
			success: true,
			message: 'Configuration updated successfully'
		};

			mockFetch.mockResolvedValueOnce({
				ok: true,
				json: () => Promise.resolve(mockResponse)
			});

			const result = await configStore.updateConfig(configData);

			expect(mockFetch).toHaveBeenCalledWith('http://localhost:8000/api/config/update', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(configData)
			});
			expect(result).toEqual(mockResponse);
		});

		it('handles update errors', async () => {
			const configData = { system: { name: 'Invalid' } };
			const errorResponse: { success: boolean; error: string } = {
				success: false,
				error: 'Validation failed'
			};

			mockFetch.mockResolvedValueOnce({
				ok: false,
				status: 400,
				json: () => Promise.resolve(errorResponse)
			});

			const result = await configStore.updateConfig(configData);

			expect(result).toEqual({
				success: false,
				error: 'Validation failed'
			});
		});
	});

	describe('resetConfig', () => {
		it('successfully resets configuration', async () => {
			const mockResponse: { success: boolean; message: string } = {
			success: true,
			message: 'Configuration reset to defaults'
		};

			mockFetch.mockResolvedValueOnce({
				ok: true,
				json: () => Promise.resolve(mockResponse)
			});

			const result = await configStore.resetConfig();

			expect(mockFetch).toHaveBeenCalledWith('http://localhost:8000/api/config/reset', {
				method: 'POST'
			});
			expect(result).toEqual(mockResponse);
		});
	});

	describe('validateConfig', () => {
		it('validates configuration without data', async () => {
			const mockResponse: { success: boolean; valid: boolean; results: Array<{ section: string; valid: boolean; message: string }> } = {
			success: true,
			valid: true,
			results: [
				{ section: 'system', valid: true, message: 'Valid' }
			]
		};

			mockFetch.mockResolvedValueOnce({
				ok: true,
				json: () => Promise.resolve(mockResponse)
			});

			const result = await configStore.validateConfig();

			expect(mockFetch).toHaveBeenCalledWith('http://localhost:8000/api/config/validate', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				}
			});
			expect(result).toEqual(mockResponse);
		});

		it('validates configuration with provided data', async () => {
			const configData = {
				system: { name: 'Test System' }
			};

			const mockResponse: { success: boolean; valid: boolean; results: Array<{ section: string; valid: boolean; message: string }> } = {
				success: true,
				valid: true,
				results: [
					{ section: 'system', valid: true, message: 'Valid' }
				]
			};

			mockFetch.mockResolvedValueOnce({
				ok: true,
				json: () => Promise.resolve(mockResponse)
			});

			const result = await configStore.validateConfig(configData);

			expect(mockFetch).toHaveBeenCalledWith('http://localhost:8000/api/config/validate', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(configData)
			});
			expect(result).toEqual(mockResponse);
		});

		it('handles validation errors', async () => {
			const configData = { invalid: 'data' };
			const errorResponse: { success: boolean; valid: boolean; error: string } = {
				success: false,
				valid: false,
				error: 'Invalid configuration'
			};

			mockFetch.mockResolvedValueOnce({
				ok: false,
				status: 400,
				json: () => Promise.resolve(errorResponse)
			});

			const result = await configStore.validateConfig(configData);

			expect(result).toEqual({
				success: false,
				error: 'Invalid configuration'
			});
		});
	});

	describe('getConfigSchema', () => {
		it('successfully gets configuration schema', async () => {
			const mockResponse: { success: boolean; data: Record<string, unknown> } = {
			success: true,
			data: {
				system: {
					type: 'object',
					properties: {
						name: { type: 'string' }
					}
					}
				}
			};

			mockFetch.mockResolvedValueOnce({
				ok: true,
				json: () => Promise.resolve(mockResponse)
			});

			const result = await configStore.getConfigSchema();

			expect(mockFetch).toHaveBeenCalledWith('http://localhost:8000/api/config/schema');
			expect(result).toEqual(mockResponse);
		});
	});
});