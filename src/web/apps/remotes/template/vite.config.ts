import { defineConfig /*, loadEnv */ } from "vite";
import react from "@vitejs/plugin-react";
import { federation } from "@module-federation/vite";
import tailwindcss from "@tailwindcss/vite";
import path from "path";

const SERVICE_NAME = "remote-template";
const SERVICE_TYPE = "ui";
const SERVICE_VERSION = "v1";
const SERVICE_PORT = 2001;

const EXPOSES = {
  "./store": "./src/store/index.ts",
  "./App": "./src/App.tsx",
  "./Counter": "./src/components/Counter.tsx",
};

// https://vite.dev/config/
export default defineConfig(({ /* command, */ /* mode */ }) => {
  const basePath = `${SERVICE_TYPE}/${SERVICE_VERSION}/${SERVICE_NAME}`;
  // const env = loadEnv(mode, process.cwd());//, "");

  return {
    // TODO base: BASE_PATH,
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
