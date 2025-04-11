import { writable } from 'svelte/store';
import type { Location } from '$lib/types/location';
import { DEFAULT_LOCATION } from '$lib/types/location';

export const location = writable<Location>(DEFAULT_LOCATION); 