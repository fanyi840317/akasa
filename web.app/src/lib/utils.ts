import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
	// alert(twMerge(clsx(inputs)));
	return twMerge(clsx(inputs));
}
export function anyify(obj: unknown) {
	return obj as any;
}

export function createDebouncedCallback<T extends (...args: any[]) => any>(
	callback: T,
	delay: number
) {
	let timeout: ReturnType<typeof setTimeout> | null = null;
	return (...args: Parameters<T>) => {
		if (timeout) clearTimeout(timeout);
		timeout = setTimeout(() => callback(...args), delay);
	};
}
export function isBrowser() {
	return typeof window !== 'undefined';
}
export const noop = () => {
	// do nothing
};
export function isValidUrl(url: string) {
	try {
		new URL(url);
		return true;
	} catch (e) {
		return false;
	}
}
export function getUrlFromString(str: string) {
	if (isValidUrl(str)) return str;
	try {
		if (str.includes('.') && !str.includes(' ')) {
			return new URL(`https://${str}`).toString();
		}
	} catch (e) {
		return null;
	}
}