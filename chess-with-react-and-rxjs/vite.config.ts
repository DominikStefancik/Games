import * as path from 'path';
import {defineConfig, loadEnv} from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig(({ command, mode }) => {
  // Load env file based on `mode` in the current working directory.
  // Set the third parameter to '' to load all env regardless of the `VITE_` prefix.
  const env = loadEnv(mode, process.cwd(), '');

  return {
    plugins: [react()],
    server: { port: Number(env.PORT), strictPort: true },
    preview: { port: Number(env.PORT), strictPort: true },
    // we have to explicitly define 'process.env', because VITE doesn't have access to env variables without prefix VITE_
    // and if we reference 'process' from anywhere in the code the 'ReferenceError: process is not defined' is thrown
    define: { 'process.env': env },
    build: { chunkSizeWarningLimit: 4096 },
    resolve: {
      alias: {
        '@local/root': path.join(__dirname, 'src'),
      },
    },
  }
})
