import BookOpen from "lucide-svelte/icons/book-open";
import Bot from "lucide-svelte/icons/bot";
import ChartPie from "lucide-svelte/icons/chart-pie";
import Frame from "lucide-svelte/icons/frame";
import LifeBuoy from "lucide-svelte/icons/life-buoy";
import Map from "lucide-svelte/icons/map";
import Send from "lucide-svelte/icons/send";
import Settings2 from "lucide-svelte/icons/settings-2";
import SquareTerminal from "lucide-svelte/icons/square-terminal";
import Activity from "lucide-svelte/icons/activity";
import type { NavItem, Project, User } from "$lib/components/console/types";

/**
 * 应用导航数据配置
 * 采用Notion风格的组织结构和命名惯例
 */
export const navData = {
  user: {
    name: "shadcn",
    email: "m@example.com",
    avatar: "/avatars/shadcn.jpg",
  } as User,
  
  navMain: [
    {
      title: "控制台",
      url: "/console/home",
      icon: SquareTerminal,
      isActive: true,
    },
    {
      title: "事件管理",
      url: "/console/events",
      icon: Activity,
      items: [
        {
          title: "事件列表",
          url: "/console/events/list",
        },
        {
          title: "事件分析",
          url: "/console/events/analysis",
        },
      ],
    },
    {
      title: "地图",
      url: "/console/map",
      icon: Map,
    },
    {
      title: "数据统计",
      url: "/console/analytics",
      icon: ChartPie,
    },
  ] as NavItem[],
  
  navSecondary: [
    {
      title: "文档",
      url: "#",
      icon: BookOpen,
    },
    {
      title: "设置",
      url: "#",
      icon: Settings2,
    },
  ] as NavItem[],
  
  projects: [
    {
      name: "Genesis",
      url: "#",
      color: "sky",
    },
    {
      name: "Explorer",
      url: "#",
      color: "violet",
    },
    {
      name: "Playground",
      url: "#",
      color: "amber",
    },
  ] as Project[],
};
