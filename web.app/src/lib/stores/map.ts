import { writable } from 'svelte/store';

interface MapMarker {
  position: [number, number];
  color: string;
  size: number;
  className?: string;
  data?: any;
}

interface MapStore {
  markers: MapMarker[];
  addMarker: (marker: MapMarker) => void;
  removeAllMarkers: () => void;
}

function createMapStore() {
  const { subscribe, set, update } = writable<MapMarker[]>([]);

  return {
    subscribe,
    addMarker: (marker: MapMarker) => update(markers => [...markers, marker]),
    removeAllMarkers: () => set([])
  };
}

export const mapStore = createMapStore(); 