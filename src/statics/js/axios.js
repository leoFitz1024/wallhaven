import axios from "axios";
import {ElMessage} from 'element-plus'


axios.defaults.baseURL = 'https://wallhaven.cc/api/v1' //正式
// axios.defaults.baseURL = 'http://test' //测试

//post请求头
axios.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded;charset=UTF-8";
//设置超时
axios.defaults.timeout = 20000;

axios.interceptors.request.use(
    config => {
        return config;
    },
    error => {
        return Promise.reject(error);
    }
);

axios.interceptors.response.use(
    response => {
        switch (response.status) {
            case 200:
                return Promise.resolve(response);
            default:
                return Promise.reject(response);
        }
    },
    error => {
        if (error.response && error.response.status === 401) {
            return Promise.resolve(error.response.data);
        } else {
            ElMessage({
                message: `请求失败，请检查网络环境和代理设置：${JSON.stringify(error.message)}`,
                type: 'error',
                duration: 2000
            })
        }
    }
);
export default {
    baseURL: axios.defaults.baseURL,
    post(url, data) {
        return new Promise((resolve, reject) => {
            axios({
                method: 'post',
                url,
                data: JSON.stringify(data),
            }).then((res) => {
                if (res.data) {
                    resolve(res.data)
                } else {
                    resolve(res.error)
                }
            }).catch(err => {
                reject(err)
            });
        })
    },
    get(url, data) {
        return new Promise((resolve, reject) => {
            axios({
                method: 'get',
                url,
                params: data,
            }).then((res) => {
                if (res) {
                    if (res.data) {
                        resolve(res.data)
                    } else {
                        resolve(res.error)
                    }
                } else {
                    resolve(res)
                }
            }).catch(err => {
                reject(err)
            })
        })
    }
};
