import { writable } from 'svelte/store';
import type { Location } from '$lib/types/location.types';
import { DEFAULT_LOCATION } from '$lib/types/location.types';

export const location = writable<Location>(DEFAULT_LOCATION); 