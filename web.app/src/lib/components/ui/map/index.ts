import MapBase from './map-base.svelte';
import MapFloat from './map-float.svelte';
import LocationPicker from './location-picker.svelte';

export type LocationData = {
  longitude: number;
  latitude: number;
};

export type LocationChangeEvent = {
  address: string;
  location: LocationData;
};

export {
  MapBase,
  MapFloat,
  LocationPicker
}; 