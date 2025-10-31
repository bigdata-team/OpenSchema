/*
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarHeader,
} from "@/components/ui/sidebar"

export function AppSidebar() {
  return (
    <Sidebar>
      <SidebarHeader />
      <SidebarContent>
        <SidebarGroup />
        <SidebarGroup />
      </SidebarContent>
      <SidebarFooter />
    </Sidebar>
  )
}
*/

// import { Calendar, Home, Inbox, Search, Settings } from "lucide-react"
// import { Home, Code, Inbox } from "lucide-react"
import { Book } from "lucide-react"
import { Link, useLocation } from "react-router"
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar"
import { useEffect, useState } from "react";
import { chatManager } from 'chat/model'
import { useNotificationStore } from 'chat/store'

// Menu items.
/* TODO
const items = [
  {
    title: "Home",
    url: "/",
    icon: Home,
  },
  {
    title: "Chat",
    url: "/chat",
    icon: Code,
  },
  {
    title: "About",
    url: "/about",
    icon: Inbox,
  },
  //{
  //  title: "Inbox",
  //  url: "#",
  //  icon: Inbox,
  //},
  //{
  //  title: "Calendar",
  //  url: "#",
  //  icon: Calendar,
  //},
  //{
  //  title: "Search",
  //  url: "#",
  //  icon: Search,
  //},
  //{
  //  title: "Settings",
  //  url: "#",
  //  icon: Settings,
  //},
]
  */

export function AppSidebar() {
  const [items, setItems] = useState<Array<{ title: string; url: string; icon: typeof Book | null }>>([]);
  const titlesChanged = useNotificationStore((state:any) => state.titlesChanged);
  const location = useLocation();

  useEffect(() => {
    const loadTitles = async () => {
      // Wait for ChatManager to finish initialization
      // TODO await chatManager.waitForInitialization();

      const titles = await chatManager.getTitles();
      console.log("AppSidebar mounted - ChatManager initialized", titles.length);

      const newItems = [
        { title: "New Chat", url: "/chat", icon: Book as typeof Book | null },
      ];
      newItems.push(...titles.map((title: any) => ({
        title: title.title ?? "",
        url: `/chat?id=${title.id}`,
        icon: null as typeof Book | null,
      })));

      setItems(newItems);
    };
    loadTitles();
  }, [titlesChanged]);

  return (
    <Sidebar>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Three-Body Bot</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {items.map((item, index) => {
                // Check if this item is active by comparing the full path with search params
                const currentPath = location.pathname + location.search;
                const isActive = currentPath === item.url;

                return (
                  <SidebarMenuItem key={index}>
                    <SidebarMenuButton asChild isActive={isActive}>
                      <Link to={item.url}>
                        {item.icon && <item.icon />}
                        <span>{item.title}</span>
                      </Link>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                );
              })}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  )
}
