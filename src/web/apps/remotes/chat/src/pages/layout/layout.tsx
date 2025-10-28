/*
import { Outlet } from 'react-router';

import Sidebar from './sidebar';

export default function Layout() {
  return (
    <div style={{ display: "flex", minHeight: "100vh" }}>
      <Sidebar />
      <main style={{ flex: 1, padding: "1rem", marginLeft: "150px" }}>
        <Outlet />
      </main>
    </div>
  );
}
*/

import { Outlet } from 'react-router';
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar"
import { AppSidebar } from "./app-sidebar"

export default function Layout() {
  return (
    /*
    <SidebarProvider
      style={{
        "--sidebar-width": "10rem",
        "--sidebar-width-mobile": "10rem",
      }}
    >
    */
    <SidebarProvider>
      <AppSidebar />
      <main>
        <SidebarTrigger />
        <div style={{ padding: "1rem" }}>
          <Outlet />
        </div>
      </main>
    </SidebarProvider>
  )
}
