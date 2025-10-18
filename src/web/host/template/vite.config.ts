import { federation } from '@module-federation/vite'
import react from '@vitejs/plugin-react'
import { writeFileSync } from 'fs';
import { defineConfig, loadEnv } from 'vite'
// import { dependencies } from './package.json'
import tailwindcss from "@tailwindcss/vite"
import path from "path"
import { fileURLToPath } from "url"

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default defineConfig(({ /* command, */ mode }) => {
	const selfEnv = loadEnv(mode, process.cwd()); // The third argument '' means load all variables, not just those prefixed with VITE_
	return {
		server: {
			fs: {
				allow: ['.', '../shared'],
			},
			// port: 3000,
		},
		build: {
			target: 'chrome89',
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
				name: 'host',
				filename: 'remoteEntry.js',
				exposes: {},
				remotes: {
					remote: {
						type: 'module',
						name: 'remote',
						entry: `${selfEnv.VITE_APP_OPENSCHEMA_UI_URL}/api/v1/remote-template/remoteEntry.js`,
						entryGlobalName: 'remote',
						shareScope: 'default',
					},
					/*
					remote2: {
						type: 'module',
						name: 'remote2',
						entry: `${selfEnv.VITE_APP_OPENSCHEMA_UI_URL}/api/v1/remote-template2/remoteEntry.js`,
						entryGlobalName: 'remote2',
						shareScope: 'default',
					},
					*/
				},
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