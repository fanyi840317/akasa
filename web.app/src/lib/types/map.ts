export interface Location {
  country?: string;
  city?: string;
  region?: string;
  timezone?: string;
  latitude?: number;
  longitude?: number;
  address?: string;
}

export const DEFAULT_LOCATION: Location = {
  country: 'CN',
  city: '',
  region: '',
  timezone: 'Asia/Shanghai',
  latitude: 39.9042,
  longitude: 116.4074
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
    [key: string]: any;
  };
} 