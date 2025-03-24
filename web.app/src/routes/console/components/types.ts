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

// 页面组件属性
export interface PageProps {
  title: string;
  description?: string;
  fullWidth?: boolean;
  className?: string;
}


