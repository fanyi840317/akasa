/**
 * 控制台组件类型定义
 * 提供统一的类型接口，确保组件间数据交互的一致性
 */

// 导航项类型
export interface NavItem {
  title: string;
  url: string;
  icon: any; 
  isActive?: boolean;
  items?: SubNavItem[];
}

// 子导航项类型
export interface SubNavItem {
  title: string;
  url: string;
  icon?: any;
}

// 项目类型
export interface Project {
  name: string;
  url: string;
  icon: any; 
  color?: string;
}

// 用户类型
export interface User {
  name: string;
  email: string;
  avatar: string;
  role?: string;
}

// 地图数据类型
export interface LocationData {
  longitude: number;
  latitude: number;
  zoom?: number;
  name?: string;
}

// 页面组件属性
export interface PageProps {
  title: string;
  description?: string;
  fullWidth?: boolean;
  className?: string;
}
