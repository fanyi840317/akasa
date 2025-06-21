/**
 * Configuration store for managing system configuration
 */

interface ConfigResponse {
	success: boolean;
	data?: Record<string, unknown>;
	error?: string;
	valid?: boolean;
	results?: ValidationResult[];
	message?: string;
}

interface ValidationResult {
	section: string;
	valid: boolean;
	message: string;
	errors?: string[];
}

class ConfigStore {
	private baseUrl = 'http://localhost:8000/api/config';

	/**
	 * Load all configuration sections
	 */
	async loadConfig(): Promise<ConfigResponse> {
		try {
			const response = await fetch(`${this.baseUrl}/`);
			const result = await response.json();
			
			if (!response.ok) {
				return {
					success: false,
					error: result.error || `HTTP ${response.status}`
				};
			}
			
			return result;
		} catch (error) {
			return {
				success: false,
				error: error instanceof Error ? error.message : '网络错误'
			};
		}
	}

	/**
	 * Load system configuration
	 */
	async loadSystemConfig(): Promise<ConfigResponse> {
		try {
			const response = await fetch(`${this.baseUrl}/system`);
			const result = await response.json();
			
			if (!response.ok) {
				return {
					success: false,
					error: result.error || `HTTP ${response.status}`
				};
			}
			
			return result;
		} catch (error) {
			return {
				success: false,
				error: error instanceof Error ? error.message : '网络错误'
			};
		}
	}

	/**
	 * Load components configuration
	 */
	async loadComponentsConfig(): Promise<ConfigResponse> {
		try {
			const response = await fetch(`${this.baseUrl}/components`);
			const result = await response.json();
			
			if (!response.ok) {
				return {
					success: false,
					error: result.error || `HTTP ${response.status}`
				};
			}
			
			return result;
		} catch (error) {
			return {
				success: false,
				error: error instanceof Error ? error.message : '网络错误'
			};
		}
	}

	/**
	 * Load LLM configuration
	 */
	async loadLLMConfig(): Promise<ConfigResponse> {
		try {
			const response = await fetch(`${this.baseUrl}/llm`);
			const result = await response.json();
			
			if (!response.ok) {
				return {
					success: false,
					error: result.error || `HTTP ${response.status}`
				};
			}
			
			return result;
		} catch (error) {
			return {
				success: false,
				error: error instanceof Error ? error.message : '网络错误'
			};
		}
	}

	/**
	 * Load raw configuration from YAML files
	 */
	async loadRawConfig(): Promise<ConfigResponse> {
		try {
			const response = await fetch(`${this.baseUrl}/raw`);
			const result = await response.json();
			
			if (!response.ok) {
				return {
					success: false,
					error: result.error || `HTTP ${response.status}`
				};
			}
			
			return result;
		} catch (error) {
			return {
				success: false,
				error: error instanceof Error ? error.message : '网络错误'
			};
		}
	}

	/**
	 * Update configuration
	 */
	async updateConfig(config: Record<string, unknown>): Promise<ConfigResponse> {
		try {
			const response = await fetch(`${this.baseUrl}/update`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(config)
			});
			
			const result = await response.json();
			
			if (!response.ok) {
				return {
					success: false,
					error: result.error || `HTTP ${response.status}`
				};
			}
			
			return result;
		} catch (error) {
			return {
				success: false,
				error: error instanceof Error ? error.message : '网络错误'
			};
		}
	}

	/**
	 * Reset configuration to defaults
	 */
	async resetConfig(): Promise<ConfigResponse> {
		try {
			const response = await fetch(`${this.baseUrl}/reset`, {
				method: 'POST'
			});
			
			const result = await response.json();
			
			if (!response.ok) {
				return {
					success: false,
					error: result.error || `HTTP ${response.status}`
				};
			}
			
			return result;
		} catch (error) {
			return {
				success: false,
				error: error instanceof Error ? error.message : '网络错误'
			};
		}
	}

	/**
	 * Validate configuration
	 */
	async validateConfig(config?: Record<string, unknown>): Promise<ConfigResponse> {
		try {
			const options: RequestInit = {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				}
			};
			
			if (config) {
				options.body = JSON.stringify(config);
			}
			
			const response = await fetch(`${this.baseUrl}/validate`, options);
			const result = await response.json();
			
			if (!response.ok) {
				return {
					success: false,
					error: result.error || `HTTP ${response.status}`
				};
			}
			
			return result;
		} catch (error) {
			return {
				success: false,
				error: error instanceof Error ? error.message : '网络错误'
			};
		}
	}

	/**
	 * Get configuration schema
	 */
	async getConfigSchema(): Promise<ConfigResponse> {
		try {
			const response = await fetch(`${this.baseUrl}/schema`);
			const result = await response.json();
			
			if (!response.ok) {
				return {
					success: false,
					error: result.error || `HTTP ${response.status}`
				};
			}
			
			return result;
		} catch (error) {
			return {
				success: false,
				error: error instanceof Error ? error.message : '网络错误'
			};
		}
	}
}

// 导出单例实例
export const configStore = new ConfigStore();