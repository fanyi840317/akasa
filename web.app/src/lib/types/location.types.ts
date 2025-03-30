export interface LocationData {
    country: string;
    city: string;
    region: string;
    latitude: number;
    longitude: number;
    timezone: string;
}

export const DEFAULT_LOCATION: LocationData = {
    country: 'CN',
    city: '',
    region: '',
    latitude: 39.9042,
    longitude: 116.4074,
    timezone: 'Asia/Shanghai'
}; 