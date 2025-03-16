/**
 * 控制台组件类型定义
 * 提供统一的类型接口，确保组件间数据交互的一致性
 */

import type { SvelteComponent } from "svelte";
import type { IconProps } from "lucide-svelte";

/**
 * 导航项类型定义
 * 用于定义控制台导航菜单项的结构和行为
 */
export interface NavItem {
  // 基本属性
  title: string;                                // 导航项标题
  url?: string;                                 // 导航链接地址
  icon?: new (options: any) => SvelteComponent<IconProps>;  // 导航图标组件
  size?: 'sm' | 'md' | 'lg' | 'xl';            // 导航项尺寸
  
  // 状态属性
  isActive?: boolean;                           // 是否处于激活状态
  state?: 'default' | 'active' | 'disabled' | 'loading'; // 项目状态
  
  // 交互行为
  clickOnly?: boolean;                          // 是否仅响应点击事件
  
  // 视觉指示器
  unread?: number;                              // 未读消息数量
  badge?: number;                               // 徽章数值
  
  // 子项目 - 递归定义，子项也是NavItem类型
  items?: NavItem[];
  
  // 行为控制
  leftViewAction?: 'replace' | 'overlay' | 'split'; // 左侧视图行为类型
  onClickAction?: 'navigate' | 'toggle' | 'expand' | 'modal' | "leftView"; // 点击后的行为
  
  // 扩展数据
  metadata?: Record<string, any>;               // 自定义元数据
}

export type ShellContext = {
  showRightView: boolean;
  setShowRightView: (value: boolean) => void;
  setTemplate: (template: any) => void;
  // setLeftViewItem: (item: PersonalItem | null) => void;
};

// 用户类型
export interface User {
  name: string;
  email: string;
  avatar: string;
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

// 个人导航项类型
export interface PersonalItem extends NavItem {
  // PersonalItem已经从NavItem继承了所有属性
  // 包括unread属性用于显示未读消息数量
  // 以及其他导航相关的属性
}

