import BookOpen from "lucide-svelte/icons/book-open";
import Bot from "lucide-svelte/icons/bot";
import ChartPie from "lucide-svelte/icons/chart-pie";
import Frame from "lucide-svelte/icons/frame";
import LifeBuoy from "lucide-svelte/icons/life-buoy";
import Map from "lucide-svelte/icons/map";
import Send from "lucide-svelte/icons/send";
import Settings2 from "lucide-svelte/icons/settings-2";
import SquareTerminal from "lucide-svelte/icons/square-terminal";
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
      title: "Playground",
      url: "#",
      icon: SquareTerminal,
      isActive: true,
      items: [
        {
          title: "History",
          url: "#",
        },
        {
          title: "Starred",
          url: "#",
        },
        {
          title: "Settings",
          url: "#",
        },
      ],
    },
    {
      title: "Models",
      url: "#",
      icon: Bot,
      items: [
        {
          title: "Genesis",
          url: "#",
        },
        {
          title: "Explorer",
          url: "#",
        },
      ],
    },
    {
      title: "Map",
      url: "/event",
      icon: Map,
    },
    {
      title: "Analytics",
      url: "#",
      icon: ChartPie,
    },
  ] as NavItem[],
  
  navSecondary: [
    {
      title: "Documentation",
      url: "#",
      icon: BookOpen,
    },
    {
      title: "Settings",
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
