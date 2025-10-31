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

import React from "react";
import { Outlet } from 'react-router';
// import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar"

// TODO import { AppSidebar } from "./app-sidebar"
// import { AppSidebar } from "./AppSidebar";
// when export default
// const AppSidebar = React.lazy(() => import('chat/AppSidebar')); // when export default
// when not export default
/*
const AppSidebar = React.lazy(() =>
  import('chat/AppSidebar').then(module => ({ default: module.AppSidebar }))
);
const SidebarProvider = React.lazy(() =>
  import('chat/sidebar').then(module => ({ default: module.SidebarProvider }))
);
const SidebarTrigger = React.lazy(() =>
  import('chat/sidebar').then(module => ({ default: module.SidebarTrigger }))
);
*/
const AppSidebarProvider = React.lazy(() =>
  import('chat/AppSidebarProvider').then(module => ({ default: module.AppSidebarProvider }))
);

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
   /*
    <React.Suspense fallback={<div>Loading...</div>}>
      <SidebarProvider>
        <AppSidebar />
        <main>
          <SidebarTrigger />
          <div style={{ padding: "0rem" }}>
            <Outlet />
          </div>
        </main>
      </SidebarProvider>
    </React.Suspense>
    */
   <AppSidebarProvider>
      <div style={{ padding: "0rem" }}>
        <Outlet />
      </div>
    </AppSidebarProvider>
  )
}
