import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
import * as path from "path";

// https://vitejs.dev/config/
export default () => defineConfig({
    base: './',
    server: {
        port: 8080,
    },
    plugins: [
        vue()
    ],
    define: {
        "APP_VERSION": JSON.stringify(process.env.npm_package_version),
    },
    build: {
        outDir: path.join(__dirname, 'dist/'),
        assetsDir: '', // 相对路径 加载问题
    },
    optimizeDeps: {
        // exclude: ['electron'], // 告诉 Vite 不要转换 electron 模块
    },
})
