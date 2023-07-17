import IPC from "../../../electron/common/updateIPC"
/**
 * 监听更新消息
 */
export const onUpdateMessage = (showUpdateMessage) => {
    window.ipcRenderer.on(IPC.UPDATE_AVAILABLE, function (info) {
        console.log("检测到新版本:" + info.version)
        showUpdateMessage(info)
    })
}

export const onUpdateErrorMessage = (showUpdateErrorMessage) => {
    window.ipcRenderer.on(IPC.UPDATE_ERROR, function (error) {
        console.log("更新失败:" + error)
        showUpdateErrorMessage(error)
    })
}

/**
 * 发送下载更新通知
 */
export const sendDownloadUpdate = () => {
    window.ipcRenderer.send(IPC.DOWNLOAD_UPDATE, {})
}

/**
 * 监听更新下载进度消息
 */
export const onDownloadProgress = (updateVersionDownloadProgress) => {
    window.ipcRenderer.on(IPC.UPDATE_DOWNLOAD_PROGRESS, function (progress) {
        updateVersionDownloadProgress(info)
    })
}
