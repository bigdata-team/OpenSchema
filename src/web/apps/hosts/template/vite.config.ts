import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";
import { federation } from "@module-federation/vite";
import tailwindcss from "@tailwindcss/vite";
import path from "path";

const SERVICE_NAME = "host-template";
const SERVICE_TYPE = "ui";
const SERVICE_VERSION = "v1";
const SERVICE_PORT = 2100;

export default defineConfig(({ command, mode }) => {
  const env = loadEnv(mode, process.cwd());//, "");

  const UI_GATEWAY_URL = env.VITE_UI_GATEWAY_URL || "http://localhost.TODO";
  const REMOTES = {
    remote: {
      name: "remote",
      entryBuild: `${UI_GATEWAY_URL}/ui/v1/remote-template/assets/remoteEntry.js`,
      entryDevel: "http://localhost:2001/ui/v1/remote-template/assets/remoteEntry.js",
      type: "module",
    },
  }
  const basePath = `${SERVICE_TYPE}/${SERVICE_VERSION}/${SERVICE_NAME}`;
  const isDev = command === "serve";

  const remotes = Object.fromEntries(
    Object.entries(REMOTES).map(([name, config]) => [
      name,
      {
        name: config.name,
        entry: isDev ? config.entryDevel : config.entryBuild,
        type: config.type,
      },
    ])
  );

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
      assetsDir: `${basePath}/assets`,
      // modulePreload: false,
    },
    plugins: [
      react(),
      tailwindcss(),
      federation({
        name: SERVICE_NAME,
        filename: `${basePath}/assets/remoteEntry.js`,
        exposes: {},
        remotes,
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
