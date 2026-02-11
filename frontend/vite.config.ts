import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
    plugins: [react()],
    server: {
        port: 5173,
        host: '127.0.0.1',  // Force IPv4
        proxy: {
            '/api': {
                target: process.env.VITE_API_URL || 'http://127.0.0.1:8000',  // Use IPv4 address
                changeOrigin: true,
            },
        },
    },
    build: {
        outDir: 'dist',
        sourcemap: false,
        rollupOptions: {
            output: {
                manualChunks: {
                    vendor: ['react', 'react-dom'],
                }
            }
        }
    }
})
