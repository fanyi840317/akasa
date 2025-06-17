import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
	return twMerge(clsx(inputs));
}

// 格式化函数
export function formatDate(date: string | Date | undefined, options?: {
	includeTime?: boolean;
	includeYear?: boolean;
	includeWeekday?: boolean;
}): string {
	if (!date) return 'No date';
	
	try {
		const d = typeof date === 'string' ? new Date(date) : date;
		if (isNaN(d.getTime())) return 'Invalid date';
		
		const formatOptions: Intl.DateTimeFormatOptions = {
			month: options?.includeYear ? 'long' : 'short',
			day: 'numeric'
		};
		
		if (options?.includeYear) {
			formatOptions.year = 'numeric';
		}
		
		if (options?.includeWeekday) {
			formatOptions.weekday = 'long';
		}
		
		if (options?.includeTime) {
			formatOptions.hour = '2-digit';
			formatOptions.minute = '2-digit';
		}
		
		return d.toLocaleDateString('zh-CN', formatOptions);
	} catch {
		return 'Invalid date';
	}
}

export function formatLocation(locationData: any): string {
	if (!locationData) return 'No location';
	
	if (typeof locationData === 'string') {
		try {
			locationData = JSON.parse(locationData);
		} catch {
			return 'Invalid location data';
		}
	}
	
	// 确保解析后的数据不为null且是对象
	if (!locationData || typeof locationData !== 'object') {
		return 'No location';
	}
	
	// 安全地访问属性
	if (locationData.address) return locationData.address;
	if (locationData.name) return locationData.name;
	return 'Unknown location';
}

// 上传相关接口定义
export interface UploadResponse {
	success: boolean;
	data?: {
		url: string;
		delete_url?: string;
		thumb: {
			url: string;
		};
	};
	error?: {
		message: string;
	};
}

export interface UploadProgress {
	loaded: number;
	total: number;
	percentage: number;
}

export type ProgressCallback = (progress: UploadProgress) => void;

// 上传到 ImgBB 的函数
export async function uploadToImgBB(
	file: File,
	onProgress?: ProgressCallback
): Promise<UploadResponse> {
	const API_KEY = 'dc1398dd7ba5dc154d50c82c42bf18c6';
	const formData = new FormData();
	formData.append('image', file);

	return new Promise((resolve, reject) => {
		const xhr = new XMLHttpRequest();

		xhr.open('POST', `https://api.imgbb.com/1/upload?key=${API_KEY}`, true);

		xhr.upload.addEventListener('progress', (event) => {
			if (event.lengthComputable && onProgress) {
				const progress: UploadProgress = {
					loaded: event.loaded,
					total: event.total,
					percentage: Math.round((event.loaded / event.total) * 100)
				};
				onProgress(progress);
			}
		});

		xhr.addEventListener('load', () => {
			if (xhr.status >= 200 && xhr.status < 300) {
				try {
					const result = JSON.parse(xhr.responseText);
					resolve(result);
					// eslint-disable-next-line @typescript-eslint/no-unused-vars
				} catch (e) {
					reject(new Error('Failed to parse response'));
				}
			} else {
				reject(new Error(`HTTP error: ${xhr.status} ${xhr.statusText}`));
			}
		});

		xhr.addEventListener('error', () => {
			reject(new Error('Network error'));
		});

		xhr.send(formData);
	});
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export type WithoutChild<T> = T extends { child?: any } ? Omit<T, 'child'> : T;
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export type WithoutChildren<T> = T extends { children?: any } ? Omit<T, 'children'> : T;
export type WithoutChildrenOrChild<T> = WithoutChildren<WithoutChild<T>>;
export type WithElementRef<T, U extends HTMLElement = HTMLElement> = T & { ref?: U | null };
