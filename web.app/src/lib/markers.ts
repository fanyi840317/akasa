export interface Marker {
  id: string;
  name: string;
  coordinates: [number, number];
  description: string;
}

export const markers: Marker[] = [
  {
    id: '1',
    name: '春熙路',
    coordinates: [104.0714, 30.6587],
    description: '成都市中心商业区'
  },
  {
    id: '2',
    name: '宽窄巷子',
    coordinates: [104.0619, 30.6703],
    description: '成都著名的历史文化街区'
  },
  {
    id: '3',
    name: '都江堰',
    coordinates: [103.6167, 30.9985],
    description: '世界文化遗产'
  },
  {
    id: '4',
    name: '大熊猫繁育研究基地',
    coordinates: [104.1437, 30.7348],
    description: '大熊猫保护研究中心'
  }
]; 