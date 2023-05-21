

/**
 * 启动app
 * @param {*} viewData
 * @param {*} obj 启动参数
 */
export const start = (obj, viewData) => {
    window.ipcRenderer.send('start', obj)
    window.ipcRenderer.once(`start`, (data) => {
        let response = JSON.parse(data)
        localStorage.setItem('download_dir', response.downloads)
        viewData.desktopInfo = response.desktopInfo
    })
}

/**
 * 获取本地文件
 * @param {*} params
 */
export const getLocalData = (params) => {
    window.ipcRenderer.send('get-local-data', params)
    return new Promise((resolve, reject) => {
        window.ipcRenderer.once(`get-local-data-receive`, (data) => resolve(data))
    })
}

/**
 * 更新在线切换参数
 * @param {*} params
 */
export const updatePageParams = (params) => {
    window.ipcRenderer.send('update-page-params', params)
    return new Promise((resolve, reject) => {
        window.ipcRenderer.once(`update-page-params-receive`, (data) => resolve(data))
    })
}

/**
 * 更新设置
 * @param {*} params
 */
export const updateConfig = (params) => {
    window.ipcRenderer.send('update-config', params)
    return new Promise((resolve, reject) => {
        window.ipcRenderer.once(`update-config-receive`, (data) => resolve(data))
    })
}

/**
 * 清除应用数据
 * @param {*} params
 */
export const clearData = () => {
    window.ipcRenderer.send('clear-data', {})
}


/**
 * 设置壁纸
 * @param {*} data
 */
export const changeBg = (data) => {
    window.ipcRenderer.send('change-bg', data)
    return new Promise((resolve, reject) => {
        window.ipcRenderer.once(`change-bg-receive`, (data) => resolve(data))
    })
}

/**
 * 选择文件夹
 * @param {*} data
 */
export const showOpenDialogSync = (data) => {
    window.ipcRenderer.send('show-open-dialog-sync', data)
    return new Promise((resolve, reject) => {
        window.ipcRenderer.once(`show-open-dialog-receive`, (data) => resolve(data))
    })
}

/**
 * 打开文件夹
 * @param {*} data
 */
export const openFolder = (data) => {
    window.ipcRenderer.send('open-folder', data)
    return new Promise((resolve, reject) => {
        window.ipcRenderer.once(`open-folder-receive`, (data) => resolve(data))
    })
}

/**
 * 删除文件
 * @param {*} path
 */
export const deleteFile = (path) => {
    window.ipcRenderer.send('delete-file', path)
    return new Promise((resolve, reject) => {
        window.ipcRenderer.once(`delete-file-receive`, (data) => resolve(data))
    })
}

/**
 * 打开文件所在位置
 * @param {*} data
 */
export const showItemInFolder = (data) => {
    window.ipcRenderer.send('show-item-in-folder', data)
    return new Promise((resolve, reject) => {
        window.ipcRenderer.once(`show-item-in-folder-receive`, (data) => resolve(data))
    })
}

export const minWindow = () => {
    window.ipcRenderer.send('min')
}

export const maxWindow = () => {
    window.ipcRenderer.send('max')
}

export const closeWindow = () => {
    window.ipcRenderer.send('close')
}

