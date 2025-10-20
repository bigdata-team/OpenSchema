import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { federation } from "@module-federation/vite";
import tailwindcss from "@tailwindcss/vite";
import path from "path";

const SERVICE_NAME = "multichat";
const SERVICE_TYPE = "ui";
const SERVICE_VERSION = "v1";
const SERVICE_PORT = 2100;

const REMOTES = {
  auth: {
    name: "auth",
    entry: "http://ui.openschema.io/ui/v1/auth/remoteEntry.js",
    type: "module",
  },
  chat: {
    name: "chat",
    entry: "http://ui.openschema.io/ui/v1/chat/remoteEntry.js",
    type: "module",
  },
};

export default defineConfig(() => {
  const basePath = `${SERVICE_TYPE}/${SERVICE_VERSION}/${SERVICE_NAME}`;

  return {
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
      assetsDir: basePath,
    },
    plugins: [
      react(),
      tailwindcss(),
      federation({
        name: SERVICE_NAME,
        filename: `${basePath}/remoteEntry.js`,
        exposes: {},
        remotes: REMOTES,
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
