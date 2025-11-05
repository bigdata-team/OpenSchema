/*
declare module "remote/App";
declare module "remote/Counter";
declare module "remote/store";
*/

declare module "chat/store";
declare module "chat/App";
declare module "chat/Counter";
declare module "chat/ChatOne";
declare module "chat/ChatSend";
declare module "chat/ChatMultiTest";
declare module "chat/ChatMulti";
declare module "chat/ChatModelSelect";
declare module "chat/model";
declare module "chat/AppSidebar";
declare module "chat/Layout";
/*
declare module "chat/sidebar" {
  import React from 'react';

  export const SidebarProvider: React.ComponentType<React.PropsWithChildren<{
    defaultOpen?: boolean;
    open?: boolean;
    onOpenChange?: (open: boolean) => void;
    className?: string;
    style?: React.CSSProperties;
  }>>;

  export const SidebarTrigger: React.ComponentType<React.ComponentProps<'button'>>;

  export const useSidebar: () => {
    state: "expanded" | "collapsed";
    open: boolean;
    setOpen: (open: boolean) => void;
    openMobile: boolean;
    setOpenMobile: (open: boolean) => void;
    isMobile: boolean;
    toggleSidebar: () => void;
  };
}
*/
declare module "chat/sidebar" {
  export const SidebarProvider: React.ComponentType<React.PropsWithChildren<any>>;
  export const SidebarTrigger: React.ComponentType;
  // ... other exports
}

declare module "chat/AppSidebarProvider" {
  export const AppSidebarProvider: React.ComponentType<React.PropsWithChildren<any>>;
}

declare module "auth/App";
declare module "auth/Counter";
declare module "auth/store";
declare module "auth/Login";
declare module "auth/AuthContext" {
  export const AuthContext: React.ComponentType<React.PropsWithChildren<any>>;
  export const AuthProvider: React.ComponentType<React.PropsWithChildren<any>>;
  export const useAuth: () => {
    user: any;
    isInitializing: boolean;
    logout: () => void;
    // ... other properties and methods
  };
}
declare module "auth/ProtectedRoute";