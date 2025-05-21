export interface Location {
  country?: string;
  city?: string;
  region?: string;
  timezone?: string;
  coordinates?: {lat: number; lng : number}|null;
  name?: string;
  description?: string;
}

export const DEFAULT_LOCATION: Location = {
  country: 'CN',
  city: '',
  region: '',
  timezone: 'Asia/Shanghai',
  coordinates: { lat: 39.9042, lng: 116.4074 },
}; 
export interface MapMarker {
  position: [number, number];
  color?: string;
  category?: string;
  className?: string;
  data?: {
    title?: string;
    location?: string;
    amount?: number;
    [key: string]: unknown;
  };
} 