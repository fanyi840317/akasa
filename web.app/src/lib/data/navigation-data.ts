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
      url: "/console",
      icon: SquareTerminal,
    },
    {
      title: "神秘事件",
      url: "/console/events",
      icon: Activity
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
      url: "/console/settings",
      clickOnly: true,
      onClickAction: "modal",
    },
  ],
  
  personalItems: [
    {
      title: "关注的人",
      icon: Heart,
      url: "/console/following"
    },
    {
      title: "收藏",
      icon: Bookmark,
      url: "/console/bookmarks"
    },
    {
      title: "调查组",
      icon: MessageSquare,
      url: "/console/teams",
      badge: 5
    }
  ],
};
