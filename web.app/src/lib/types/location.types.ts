export interface Location {
    country: string;
    city: string;
    region: string;
    timezone: string;
    latitude: number;
    longitude: number;
}

export const DEFAULT_LOCATION: Location = {
    country: 'CN',
    city: '',
    region: '',
    timezone: 'Asia/Shanghai',
    latitude: 39.9042,
    longitude: 116.4074
}; 