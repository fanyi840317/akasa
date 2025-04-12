import { PUBLIC_MAPBOX_TOKEN } from '$env/static/public';

export interface LocationData {
  longitude: number;
  latitude: number;
  city?: string;
  region?: string;
  country_code?: string;
  country?: string;
}

export interface LocationResult {
  location: LocationData;
  address: string;
}

let locationData: LocationData | null = null;

// 默认位置（成都）
const DEFAULT_LOCATION: LocationData = {
  latitude: 30.67,
  longitude: 104.06,
  city: '成都',
  region: '四川',
  country_code: 'CN',
  country: 'China'
};

// 统一的反向地理编码函数
export async function reverseGeocodeLocation(lat: number, lon: number): Promise<string> {
  try {
    const response = await fetch(
      `https://api.mapbox.com/geocoding/v5/mapbox.places/${lon},${lat}.json?access_token=${PUBLIC_MAPBOX_TOKEN}&language=zh`
    );

    if (!response.ok) {
      throw new Error("地理编码请求失败");
    }

    const data = await response.json();
    if (!data.features || data.features.length === 0) {
      return `${lat.toFixed(6)}, ${lon.toFixed(6)}`;
    }

    return data.features[0].place_name;
  } catch (error) {
    console.error("反向地理编码失败:", error);
    return `${lat.toFixed(6)}, ${lon.toFixed(6)}`;
  }
}

// 使用 IP 获取位置
export async function getLocationByIP() {
  try {
    const response = await fetch("https://ipapi.co/json/");
    if (!response.ok) {
      throw new Error("IP 定位请求失败");
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("IP 定位失败:", error);
    throw error;
  }
}

// 使用浏览器定位
async function getLocationByBrowser(): Promise<LocationResult> {
  if (!("geolocation" in navigator)) {
    throw new Error("浏览器不支持地理定位");
  }

  const position = await new Promise<GeolocationPosition>((resolve, reject) => {
    console.log("浏览器定位开始");
    navigator.geolocation.getCurrentPosition(resolve, reject, {
      timeout: 1000000,
      maximumAge: 0,
      enableHighAccuracy: true,
    });
    console.log("浏览器定位成功");
  });

  const { latitude, longitude } = position.coords;
  const locationData = { longitude, latitude };
  const address = await reverseGeocodeLocation(latitude, longitude);

  return {
    location: locationData,
    address
  };
}

export async function getCurrentLocation(): Promise<LocationResult> {
  return getLocationByBrowser()
    .catch(error => {
      console.log("浏览器定位失败，尝试使用IP定位:", error);
      return getLocationByIP()
        .then(ipLocation => 
          reverseGeocodeLocation(ipLocation.latitude, ipLocation.longitude)
            .then(address => ({
              location: ipLocation,
              address
            }))
        )
        .catch(error => {
          console.error("IP定位失败，使用默认位置:", error);
          return {
            location: DEFAULT_LOCATION,
            address: `${DEFAULT_LOCATION.city}, ${DEFAULT_LOCATION.region}`
          };
        });
    });
}

export async function getLocationData(): Promise<LocationData> {
  if (locationData) {
    return locationData;
  }

  try {
    const result = await getCurrentLocation();
    locationData = result.location;
    return locationData;
  } catch (error) {
    console.error('获取位置信息失败:', error);
    locationData = DEFAULT_LOCATION;
    return locationData;
  }
}

// 导出反向地理编码函数供外部使用
export { reverseGeocodeLocation as reverseGeocode };
