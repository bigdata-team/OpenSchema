import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { federation } from "@module-federation/vite";
import tailwindcss from "@tailwindcss/vite";
import path from "path";

const SERVICE_NAME = "host-template";
const SERVICE_TYPE = "ui";
const SERVICE_VERSION = "v1";
const SERVICE_PORT = 2100;

const REMOTES = {
  template: {
    entry: "http://ui.openschema.io/ui/v1/remote-template/assets/remoteEntry.js",
    type: "module",
  },
};

const REMOTES_DEV = {
  template: {
    entry: "http://localhost:2001/ui/v1/remote-template/assets/remoteEntry.js",
    type: "module",
  },
};

export default defineConfig(({ command, /* mode */ }) => {
  const basePath = `${SERVICE_TYPE}/${SERVICE_VERSION}/${SERVICE_NAME}`;
  // const env = loadEnv(mode, process.cwd());//, "");

  let remotes = {};
  if (command === "serve") {
    remotes = REMOTES_DEV;
  } else {
    remotes = REMOTES;
  }

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
