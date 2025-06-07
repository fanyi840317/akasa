import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import { writable } from "svelte/store";

export function cn(...inputs: ClassValue[]) {
    // alert(twMerge(clsx(inputs)));
    return twMerge(clsx(inputs));
}
export function anyify(obj: unknown) {
    return obj as unknown;
}

export function createDebouncedCallback<T extends (...args: unknown[]) => unknown>(
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
    } catch {
        return false;
    }
}
export function getUrlFromString(str: string) {
    if (isValidUrl(str)) return str;
    try {
        if (str.includes('.') && !str.includes(' ')) {
            return new URL(`https://${str}`).toString();
        }
    } catch {
        return null;
    }
}

// i18n utilities
export const currentLang = writable('zh');

export function setLanguage(lang: string) {
    currentLang.set(lang);
}

export function getCurrentLang() {
    let currentValue = 'zh';
    currentLang.subscribe(value => {
        currentValue = value;
    })();
    return currentValue;
}

interface I18nFields {
    name?: string | { zh: string; en: string };
    description?: string | { zh: string; en: string };
    [key: string]: unknown;
}

export function parseI18nFields<T extends I18nFields>(data: T): T {
    const result = { ...data };

    // 处理 name 字段
    if (typeof result.name === 'string') {
        try {
            result.name = JSON.parse(result.name);
        } catch (e) {
            // 如果解析失败，保持原样
            console.error(e);
        }
    }

    // 处理 description 字段
    if (typeof result.description === 'string') {
        try {
            result.description = JSON.parse(result.description);
        } catch (e) {
            // 如果解析失败，保持原样
            console.error(e);
        }
    }

    return result;
}

export function stringifyI18nFields<T extends I18nFields>(data: T): T {
    const result = { ...data };

    // 处理 name 字段
    if (typeof result.name === 'object') {
        result.name = JSON.stringify(result.name);
    }

    // 处理 description 字段
    if (typeof result.description === 'object') {
        result.description = JSON.stringify(result.description);
    }

    return result;
}

type I18nValue = { zh: string; en: string } | string;
type SupportedLang = 'zh' | 'en';

export function getI18nValue(field: I18nValue, lang?: SupportedLang): string {
    if (typeof field === 'string') return field;
    return field[lang || getCurrentLang() as SupportedLang] || field.zh;
}
// 格式化创建和修改时间
export function formatSystemDate(dateStr: string) {
    const date = new Date(dateStr);
    return date.toLocaleDateString("zh-CN", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
    });
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export type WithoutChild<T> = T extends { child?: any } ? Omit<T, "child"> : T;
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export type WithoutChildren<T> = T extends { children?: any } ? Omit<T, "children"> : T;
export type WithoutChildrenOrChild<T> = WithoutChildren<WithoutChild<T>>;
export type WithElementRef<T, U extends HTMLElement = HTMLElement> = T & { ref?: U | null };
