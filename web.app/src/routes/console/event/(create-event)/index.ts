export { default as BasicInfo } from './BasicInfo.svelte';
export { default as LocationPicker } from './LocationPicker.svelte';
export { default as ImageUpload } from './ImageUpload.svelte';

export type CreateEventStep = {
    title: string;
    description: string;
    component: any;
};

export type CreateEventData = {
    title: string;
    description: string;
    location: string;
    imageFile: File | null;
};