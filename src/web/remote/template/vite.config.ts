import { federation } from '@module-federation/vite';
import react from '@vitejs/plugin-react';
import { writeFileSync } from 'fs';
import { defineConfig, loadEnv } from 'vite';
// import { dependencies } from './package.json';
import tailwindcss from "@tailwindcss/vite";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default defineConfig(({ /* command, */ mode }) => {
	const selfEnv = loadEnv(mode, process.cwd()); // The third argument '' means load all variables, not just those prefixed with VITE_
	return {
		server: {
			fs: {
				allow: ['.', '../shared'],
			},
			// port: 3009,
			// allowedHosts: [ 'localhost' ],
		},
		build: {
			target: 'chrome89',
			assetsDir: 'api/v1/remote-template',
		},
		plugins: [
			{
				name: 'generate-environment',
				options: function () {
					console.info('selfEnv', selfEnv);
					writeFileSync('./src/environment.ts', `export default ${JSON.stringify(selfEnv, null, 2)};`);
				},
			},
			react(),
			tailwindcss(),
			federation({
				name: 'remote',
				filename: 'api/v1/remote-template/remoteEntry.js',
				exposes: {
					'./remote-app': './src/App.tsx',
				},
				remotes: {},
				shared: ["react", "react-dom"],
			}),
		],
		resolve: {
  			alias: {
  		    	"@": path.resolve(__dirname, "./src"),
  		  	},
  		},
	};
});