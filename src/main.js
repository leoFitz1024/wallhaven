import {createApp} from 'vue'
import {ElMessage} from 'element-plus'
import 'element-plus/dist/index.css'
import axios from './statics/js/axios';
import App from './App.vue'
import {router} from './router'
import {formatMulti, formatFileSize, formatSpeed, formatTime} from "./statics/js/utils"

const app = createApp(App)
//全局配置
app.config.globalProperties.$message = ElMessage;
app.config.globalProperties.$formatMulti = formatMulti;
app.config.globalProperties.$formatFileSize = formatFileSize;
app.config.globalProperties.$formatSpeed = formatSpeed;
app.config.globalProperties.$formatTime = formatTime;
app.config.globalProperties.$axios = axios;
app.config.globalProperties.$imgPrefix = axios.baseURL + "/api/local/img?path="

app.use(router)
app.mount('#app')

