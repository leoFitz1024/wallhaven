const baseURL = "https://wallhaven.cc/api/v1/";


const ajax = (url) => {
    return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        xhr.open('GET', baseURL + url);
        xhr.setRequestHeader('Accept', 'application/json');
        xhr.onreadystatechange = function () {
            if (xhr.readyState !== 4) return;
            if (xhr.status === 200 || xhr.status === 304) {
                try {
                    resolve(JSON.parse(xhr.responseText));
                } catch (error) {
                    resolve(xhr.responseText);
                }
            } else {
                reject(new Error(xhr.responseText));
            }
        }
        xhr.send();
    })
}

/**
 * 获取图片数据
 * @param {*} url 文件地址
 * @param {*} timeout 超时时间
 */
export const getImgBlod = (url, timeout = 60000) => {
    return new Promise((resolve, reject) => {
        let xhr = new XMLHttpRequest();
        xhr.open("GET", url);
        xhr.responseType = "blob";

        let timedout = false;
        let timer = setTimeout(function () {
            timedout = true;
            xhr.abort();
            reject('连接超时！！！')
        }, timeout);


        xhr.onreadystatechange = function () {
            if (xhr.readyState !== 4) return;
            if (timedout) { return; }
            clearTimeout(timer);
            if (xhr.status === 200 || xhr.status === 304) {
                try {
                    let blob = this.response;
                    resolve(window.URL.createObjectURL(blob));
                }
                catch (error) {
                    reject(xhr.responseText);
                }
            } else {
                reject(new Error(xhr.responseText));
            }
        };
        xhr.send();
    })
}

export default ajax;
