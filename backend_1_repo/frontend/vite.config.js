import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    proxy: {
      '/echo': 'http://backend1:5000/',
      '/api': 'http://backend1:5000/',
    },
    hmr: {
      clientPort: 5173,
    },
    watch: {
      usePolling: true,
    },
  },
  build: {
    // root: 'app',
    outDir: 'static',
  },
})
