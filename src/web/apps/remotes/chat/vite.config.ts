import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";
import { federation } from "@module-federation/vite";
import tailwindcss from "@tailwindcss/vite";
import path from "path";

export default defineConfig(({ mode }) => {
  // const isDev = mode === "serve";
  const env = loadEnv(mode, process.cwd());

  ///////////////////////////////
  //////// Configuration ////////
  ///////////////////////////////

  const SERVICE_NAME = "chat";
  const SERVICE_TYPE = "ui";
  const SERVICE_VERSION = "v1";
  const SERVICE_PORT = 2001;
  const UI_GATEWAY_URL = env.VITE_UI_GATEWAY_URL ?? "http://localhost";

  const EXPOSES = {
    "./store": "./src/store/index.ts",
    "./App": "./src/App.tsx",
    "./Counter": "./src/components/Counter.tsx",
    "./ChatOne": "./src/components/ChatOne.tsx",
    "./ChatSend": "./src/components/ChatSend.tsx",
    "./ChatMultiTest": "./src/components/ChatMultiTest.tsx",
    "./ChatMulti": "./src/components/ChatMulti.tsx",
    "./ChatModelSelect": "./src/components/ChatModelSelect.tsx",
    "./AppSidebar": "./src/pages/layout/AppSidebar.tsx",
    "./Layout": "./src/pages/layout/Layout.tsx",
    "./sidebar": "./src/components/ui/sidebar.tsx",
    "./AppSidebarProvider": "./src/pages/layout/AppSidebarProvider.tsx",
    "./model": "./src/model/index.ts",
  };

  ///////////////////////////////

  const basePath = `${SERVICE_TYPE}/${SERVICE_VERSION}/${SERVICE_NAME}`;
  return {
    base: UI_GATEWAY_URL,
    server: {
      port: SERVICE_PORT,
      hmr: {
        protocol: "ws",
        host: "localhost",
        clientPort: SERVICE_PORT,
        path: "/__vite/ws",
      },
    },
    build: {
      target: "chrome89",
      assetsDir: `${basePath}/assets`,
    },
    plugins: [
      react(),
      tailwindcss(),
      federation({
        name: SERVICE_NAME,
        filename: `${basePath}/assets/remoteEntry.js`,
        exposes: EXPOSES,
        remotes: {},
        shared: ["react", "react-dom", "react-router"],
      }),
    ],
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "./src"),
      },
    },
  };
});
