import { writable } from 'svelte/store';
import mapboxgl from "mapbox-gl";

// Removed MapMarker interface as it's no longer used here

interface MapState {
  mapInstance: mapboxgl.Map | null;
}

function createMapStore() {
  const { subscribe, update } = writable<MapState>({
    mapInstance: null,
  });

  return {
    subscribe,
    // Method to set the current map instance
    setMapInstance: (map: mapboxgl.Map | null) =>
      update((state) => ({
        ...state,
        mapInstance: map,
      })),
    // Method to clear the map instance (e.g., when the map component unmounts)
    clearMapInstance: () =>
      update((state) => ({
        ...state,
        mapInstance: null,
      })),
    // Method to get the current map instance directly (alternative to subscribing)
    getMapInstance: (): mapboxgl.Map | null => {
      let instance: mapboxgl.Map | null = null;
      // Use subscribe with a limit to get the current value once
      const unsubscribe = subscribe(state => {
        instance = state.mapInstance;
      });
      unsubscribe(); // Immediately unsubscribe
      return instance;
    }
  };
}

export const mapStore = createMapStore();