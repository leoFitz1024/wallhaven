import {formatDate} from './date.js'

/**
 * 从localStorage取值
 * @param {*} data
 */
export const getLocalStorage = (key, defaultValue, type) => {
    let value = localStorage.getItem(key)
    if (value === null || value === "undefined") {
        console.log("key:" + key + "，初始化为默认值：" + defaultValue)
        if (type === "Object") {
            localStorage.setItem(key, JSON.stringify(defaultValue))
        } else {
            localStorage.setItem(key, defaultValue)
        }
    }
    if (value === null || value === "undefined") {
        return defaultValue
    }
    switch (type) {
        case "Number":
            value = parseInt(value)
            break
        case "Object":
            value = JSON.parse(value)
            break
        default:

    }
    return value;
}


export const formatMulti = (str) => {
    return str.replace("x", " x ");
}

export const formatFileSize = (size) => {
    if ((size / 1024.0 / 1024.0) > 1) {
        return parseFloat((size / 1024 / 1024.0).toFixed(2)) + "MB";
    } else {
        return parseInt(size / 1024.0) + "KB";
    }
}

export const formatSpeed = (speed) => {
    if ((speed / 1024.0 / 1024.0) > 1) {
        return parseFloat((speed / 1024 / 1024.0).toFixed(2)) + " MB/s";
    } else {
        return parseInt(speed / 1024.0) + " kb/s";
    }
}
export const formatTime = (timestamp) => {
    return formatDate(new Date(timestamp), 'yyyy-MM-dd hh:mm')
}

