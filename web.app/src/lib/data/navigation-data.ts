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
import { 
  Bell,
  Shield,
  Palette,
  Globe,
  KeyRound,
  CreditCard,
  HelpCircle,
  User as UserIcon,
  Inbox,
  Home,
  Heart,
  Bookmark,
  MessageSquare
} from "lucide-svelte";

import type { NavItem, PersonalItem, User } from "../../routes/console/components/types";

/**
 * 应用导航数据配置
 * 采用Notion风格的组织结构和命名惯例
 */
export const navData: {
  user: User;
  navMain: NavItem[];
  navSecondary: NavItem[];
  personalItems: PersonalItem[];
} = {
  user: {
    name: "shadcn",
    email: "m@example.com",
    avatar: "/avatars/shadcn.jpg",
  },
  
  navMain: [
    {
      title: "主页",
      url: "/console/events",
      icon: SquareTerminal,
    },
    {
      title: "地图",
      url: "/console/map",
      icon: Map,
    },
    {
      title: "收件箱",
      icon: Inbox,
      onClickAction:"leftView",
      state: "disabled",
      clickOnly: true,
      unread: 3
    }
  ],
  
  navSecondary: [
    {
      title: "反馈",
      size: "sm",
      url: "#",
      icon: BookOpen,
    },
    {
      title: "设置",
      size: "sm",
      icon: Settings2,
      state: "disabled",
      url: "/console/settings",
      clickOnly: true,
      onClickAction: "modal",
    },
  ],
  
  personalItems: [
    {
      title: "我的事件档案",
      icon: Bookmark,
      state: "disabled",
      items: [
        {
          title: "我的事件",
          icon: Bookmark,
          state: "disabled",
          url: "/console/bookmarks"
        },
        {
          title: "我的收藏",
          icon: Bookmark,
          state: "disabled",
          url: "/console/bookmarks"
        },
        {
          title: "我关注的",
          icon: Bookmark,
          state: "disabled",
          url: "/console/bookmarks"
        }
      ],
      url: "/console/bookmarks"
    },
    {
      title: "我的收藏",
      icon: Bookmark,
      state: "disabled",
      url: "/console/bookmarks"
    }
  ],
};
