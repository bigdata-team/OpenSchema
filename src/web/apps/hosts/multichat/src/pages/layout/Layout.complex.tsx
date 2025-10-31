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

import React, { useEffect, useState } from "react";
import { Outlet } from 'react-router';

// Dynamically import sidebar components from the remote to share the same React Context
export default function Layout() {
  const [sidebarComponents, setSidebarComponents] = useState<{
    SidebarProvider: React.ComponentType<React.PropsWithChildren>;
    SidebarTrigger: React.ComponentType;
  } | null>(null);

  const [AppSidebarComponent, setAppSidebarComponent] = useState<React.ComponentType | null>(null);

  useEffect(() => {
    // Load sidebar components
    import('chat/sidebar').then(module => {
      setSidebarComponents({
        SidebarProvider: module.SidebarProvider,
        SidebarTrigger: module.SidebarTrigger,
      });
    });

    // Load AppSidebar component
    import('chat/AppSidebar').then(module => {
      setAppSidebarComponent(() => module.AppSidebar);
    });
  }, []);

  if (!sidebarComponents || !AppSidebarComponent) {
    return <div>Loading Sidebar...</div>;
  }

  const { SidebarProvider, SidebarTrigger } = sidebarComponents;
  const AppSidebar = AppSidebarComponent;

  return (
    <SidebarProvider>
      <AppSidebar />
      <main>
        <SidebarTrigger />
        <div style={{ padding: "0rem" }}>
          <Outlet />
        </div>
      </main>
    </SidebarProvider>
  );
}
