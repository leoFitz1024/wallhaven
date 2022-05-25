
/**
 * 下载文件
 * @param {*} item
 */
export const downloadFile = (item) => {
    window.ipcRenderer.send('download-file', item)
    return new Promise((resolve, reject) => {
        window.ipcRenderer.once(`download-file-${item.url}`, (data) => resolve(data))
    })
}

/**
 * 更新下载状态
 * @param {*} updateData
 */
export const updateDownloadState = (updateData) => {
    window.ipcRenderer.on('update-download-state', function (data) {
        updateData(data)
    })
}

/**
 * 取消下载
 * @param {*} url
 */
export const cancelDownload = (url) => {
    window.ipcRenderer.send('download-file-cancel', url)
    return new Promise((resolve, reject) => {
        window.ipcRenderer.once(`download-file-cancel-${url}`, (data) => resolve(data))
    })
}


/**
 * 暂停下载
 * @param {*} url
 */
export const pauseDownload = (url) => {
    window.ipcRenderer.send('download-file-pause', url)
    return new Promise((resolve, reject) => {
        window.ipcRenderer.once(`download-file-pause-${url}`, (data) => resolve(data))
    })
}

/**
 * 断点下载恢复
 * @param {*} data
 */
export const resumeDownload = (data) => {
    window.ipcRenderer.send('resume-download', data)
    return new Promise((resolve, reject) => {
        window.ipcRenderer.once(`download-file-resume-${data.url}`, (data) => resolve(data))
    })
}
