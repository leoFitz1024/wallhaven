import DOWNLOAD_IPC from "../../../electron/common/downloadIPC"
/**
 * 下载文件
 * @param {*} item
 */
export const downloadFile = (item) => {
    window.ipcRenderer.send(DOWNLOAD_IPC.DOWNLOAD_FILE, item)
    return new Promise((resolve, reject) => {
        window.ipcRenderer.once(`${DOWNLOAD_IPC.DOWNLOAD_FILE}-${item.url}`, (data) => resolve(data))
    })
}

/**
 * 暂停下载
 * @param {*} url
 */
export const pauseDownload = (url) => {
    window.ipcRenderer.send(DOWNLOAD_IPC.DOWNLOAD_FILE_PAUSE, url)
    return new Promise((resolve, reject) => {
        window.ipcRenderer.once(`${DOWNLOAD_IPC.DOWNLOAD_FILE_PAUSE}-${url}`, (data) => resolve(data))
    })
}

/**
 * 更新下载状态
 * @param {*} updateData
 */
export const updateDownloadState = (updateData) => {
    window.ipcRenderer.on(DOWNLOAD_IPC.UPDATE_DOWNLOAD_STATE, function (data) {
        updateData(data)
    })
}

/**
 * 断点下载恢复
 * @param {*} data
 */
export const resumeDownload = (data) => {
    window.ipcRenderer.send(DOWNLOAD_IPC.RESUME_DOWNLOAD, data)
    return new Promise((resolve, reject) => {
        window.ipcRenderer.once(`${DOWNLOAD_IPC.RESUME_DOWNLOAD}-${data.url}`, (data) => resolve(data))
    })
}

/**
 * 取消下载
 * @param {*} url
 */
export const cancelDownload = (url) => {
    window.ipcRenderer.send(DOWNLOAD_IPC.DOWNLOAD_CANCEL, url)
    return new Promise((resolve, reject) => {
        window.ipcRenderer.once(`${DOWNLOAD_IPC.DOWNLOAD_CANCEL}-${url}`, (data) => resolve(data))
    })
}

