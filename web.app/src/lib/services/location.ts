type LocationData = {
    latitude: number;
    longitude: number;
    city: string;
    region: string;
};

export async function getUserLocation(): Promise<LocationData> {
    try {
        const response = await fetch('https://ipapi.co/json/');
        const data = await response.json();
        
        return {
            latitude: data.latitude,
            longitude: data.longitude,
            city: data.city,
            region: data.region
        };
    } catch (error) {
        console.error('获取位置信息失败:', error);
        // 默认返回成都的坐标
        return {
            latitude: 30.67,
            longitude: 104.06,
            city: '成都',
            region: '四川'
        };
    }
} 