import { init } from 'svelte-i18n';

type LocationData = {
    latitude: number;
    longitude: number;
    city: string;
    region: string;
    country_code: string;
    country: string;
};

let locationData: LocationData | null = null;

export async function getLocationData(): Promise<LocationData> {
    if (locationData) {
        return locationData;
    }

    try {
        const response = await fetch('https://ipapi.co/json/');
        const data = await response.json();
        
        locationData = {
            latitude: data.latitude,
            longitude: data.longitude,
            city: data.city,
            region: data.region,
            country_code: data.country_code,
            country: data.country
        };

        return locationData;
    } catch (error) {
        console.error('获取位置信息失败:', error);
        // 默认返回成都的坐标
        locationData = {
            latitude: 30.67,
            longitude: 104.06,
            city: '成都',
            region: '四川',
            country_code: 'CN',
            country: 'China'
        };

        return locationData;
    }
}
