import APP_IPC from "../../../electron/common/appIPC"
/**
 * 启动app
 * @param {*} viewData
 * @param {*} obj 启动参数
 */
export const start = (obj, viewData) => {
    window.ipcRenderer.send(APP_IPC.START, obj)
    window.ipcRenderer.once(APP_IPC.START, (data) => {
        let response = JSON.parse(data)
        localStorage.setItem('downloadDir', response.downloads)
        viewData.desktopInfo = response.desktopInfo
    })
}

/**
 * 获取本地文件
 * @param {*} params
 */
export const getLocalData = (params) => {
    window.ipcRenderer.send(APP_IPC.GET_DOWNLOADED_IMG, params)
    return new Promise((resolve, reject) => {
        window.ipcRenderer.once(APP_IPC.GET_DOWNLOADED_IMG, (data) => resolve(data))
    })
}

/**
 * 更新在线切换参数
 * @param {*} params
 */
export const updatePageParams = (params) => {
    window.ipcRenderer.send(APP_IPC.UPDATE_PAGE_PARAMS, params)
    return new Promise((resolve, reject) => {
        window.ipcRenderer.once(APP_IPC.UPDATE_PAGE_PARAMS, (data) => resolve(data))
    })
}

/**
 * 更新设置
 * @param {*} params
 */
export const updateConfig = (params) => {
    window.ipcRenderer.send(APP_IPC.SAVE_CONFIG, JSON.stringify(params))
    return new Promise((resolve, reject) => {
        window.ipcRenderer.once(APP_IPC.SAVE_CONFIG, (data) => resolve(data))
    })
}

/**
 * 关闭网络代理
 */
export const sendCloseProxy = () => {
    window.ipcRenderer.send(APP_IPC.CLOSE_PROXY, {})
}

/**
 * 设置壁纸
 * @param {*} data
 */
export const changeBg = (data) => {
    window.ipcRenderer.send(APP_IPC.CHANGE_BG, data)
    return new Promise((resolve, reject) => {
        window.ipcRenderer.once(APP_IPC.CHANGE_BG, (data) => resolve(data))
    })
}

/**
 * 选择文件夹
 * @param {*} data
 */
export const showOpenDialogSync = (data) => {
    window.ipcRenderer.send(APP_IPC.SELECT_FOLDER_DIALOG, data)
    return new Promise((resolve, reject) => {
        window.ipcRenderer.once(APP_IPC.SELECT_FOLDER_DIALOG, (data) => resolve(data))
    })
}

/**
 * 打开文件夹
 * @param {*} data
 */
export const openFolder = (data) => {
    window.ipcRenderer.send(APP_IPC.OPEN_FOLDER, data)
    return new Promise((resolve, reject) => {
        window.ipcRenderer.once(APP_IPC.OPEN_FOLDER, (data) => resolve(data))
    })
}

/**
 * 打开文件所在位置
 * @param {*} data
 */
export const showItemInFolder = (data) => {
    window.ipcRenderer.send(APP_IPC.SHOW_FILE_FOLDER, data)
    return new Promise((resolve, reject) => {
        window.ipcRenderer.once(APP_IPC.SHOW_FILE_FOLDER, (data) => resolve(data))
    })
}

/**
 * 删除文件
 * @param {*} path
 */
export const deleteFile = (path) => {
    window.ipcRenderer.send(APP_IPC.DELETE_FILE, path)
    return new Promise((resolve, reject) => {
        window.ipcRenderer.once(APP_IPC.DELETE_FILE, (data) => resolve(data))
    })
}

/**
 * 清除应用数据
 * @param {*} params
 */
export const clearData = () => {
    window.ipcRenderer.send(APP_IPC.CLEAR_DATA, {})
}

export const minWindow = () => {
    window.ipcRenderer.send(APP_IPC.MIN_WINDOW)
}

export const maxWindow = () => {
    window.ipcRenderer.send(APP_IPC.MAX_WINDOW)
}

export const closeWindow = () => {
    window.ipcRenderer.send(APP_IPC.CLOSE_WINDOW)
}

//默认浏览器打开链接
export const openLink = (url) => {
    window.ipcRenderer.send(APP_IPC.OPEN_LINK, url)
}

