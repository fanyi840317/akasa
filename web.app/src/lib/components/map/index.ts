import MapBase from './map-base.svelte';
import MapFloat from './map-float.svelte';
import LocationPicker from './location-picker.svelte';

export interface LocationData {
  lat: number;
  lng: number;
  address: string;
  placeId?: string;
  name?: string;
}

export interface LocationChangeEvent {
  location: LocationData;
}

export {
  MapBase,
  MapFloat,
  LocationPicker
}; 