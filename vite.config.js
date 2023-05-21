import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import * as path from "path";

// https://vitejs.dev/config/
export default () => defineConfig({
  base: './',
  server:{
    port: 8080,
    // proxy:{
    //   "/wallhavenApi":{
    //     target: "https://wallhaven.cc/api/v1/",
    //     changeOrigin: true,
    //     rewrite: (path) => path.replace(/^\/wallhavenApi/, '')
    //     }
    //   }
    },
  plugins: [vue()],
  build: {
    outDir: path.join(__dirname, 'dist/'),
    assetsDir: '', // 相对路径 加载问题
  },
  optimizeDeps: {
    // exclude: ['electron'], // 告诉 Vite 不要转换 electron 模块
  },
})
