import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";
import { federation } from "@module-federation/vite";
import tailwindcss from "@tailwindcss/vite";
import path from "path";

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");

  // const SERVICE_TYPE = env.VITE_SERVICE_TYPE ?? "ui";
  // const SERVICE_VERSION = env.VITE_SERVICE_VERSION ?? "v1";
  const SERVICE_NAME = env.VITE_SERVICE_NAME ?? "remote";

  // const BASE_PATH = `/${SERVICE_TYPE}/${SERVICE_VERSION}/${SERVICE_NAME}`;

  const hardPort = 2001;

  return {
    // TODO base: BASE_PATH,
    server: {
      port: hardPort,
      hmr: {
        protocol: "ws",
        host: "localhost",
        clientPort: parseInt(env.HMR_PORT) ?? hardPort,
        path: "/__vite/ws",
      },
    },
    build: {
      target: "chrome89",
    },
    plugins: [
      react(),
      tailwindcss(),
      federation({
        name: SERVICE_NAME,
        filename: "remoteEntry.js",
        exposes: {
          "./store": "./src/store/index.ts",
          "./App": "./src/App.tsx",
          "./Counter": "./src/components/Counter.tsx",
        },
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
