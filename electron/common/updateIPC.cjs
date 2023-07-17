/*
 * @Author: Chen
 * @Description: IPC 通信 channel 表
 */
module.exports = {
    // 开始检查更新
    CHECK_UPDATE: 'UPDATE_CHECKING',
    // 检查更新出错
    UPDATE_ERROR: 'UPDATE_ERROR',
    // 检查到新版本
    UPDATE_AVAILABLE: 'UPDATE_AVAILABLE',
    //下载更新
    DOWNLOAD_UPDATE: 'DOWNLOAD_UPDATE',
    //更新下载进度
    UPDATE_DOWNLOAD_PROGRESS: 'UPDATE_DOWNLOAD_PROGRESS',
    // 已经是新版本
    UPDATE_NOT_AVAILABLE: 'UPDATE_NOT_AVAILABLE',
}
