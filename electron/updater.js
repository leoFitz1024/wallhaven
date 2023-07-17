const {autoUpdater} = require("electron-updater");
const {ipcMain} = require('electron');
const logger = require("electron-log");
const path = require('path')
const IPC = require("./common/updateIPC.cjs");

const updaterLogger = logger.create("updater")
updaterLogger.transports.file.level = 'debug'
updaterLogger.transports.file.maxSize = 1002430 // 10M
updaterLogger.transports.file.format = '[{y}-{m}-{d} {h}:{i}:{s}.{ms}] [{level}]{scope} {text}'
updaterLogger.transports.console.format = '[{y}-{m}-{d} {h}:{i}:{s}.{ms}] [{level}]{scope} {text}'
updaterLogger.transports.file.resolvePath = () => {
    let date = new Date()
    date = date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate()
    let fileName = `${date}.log`
    return path.join("logs/update", fileName)
};

//检查更新
function checkUpdate(app, mainWindow) {
    updaterLogger.info("检查更新")
    autoUpdater.logger = updaterLogger
    //开发模式调试自动更新
    // autoUpdater.updateConfigPath = path.join(__dirname, '../dev-app-update.yml');
    autoUpdater.checkForUpdates();

    // 存在新版本时，默认自动下载更新
    autoUpdater.autoDownload = false // 若想通过渲染进程手动触发，需要设置autoDownload为false

    // 当更新发生错误的时候触发
    autoUpdater.on('error', (err) => {
        updaterLogger.error("更新失败：" + err)
        mainWindow.webContents.send(IPC.UPDATE_ERROR, err);
    })

    // // 当开始检查更新的时候触发 通知渲染进程，此时开始检测版本
    // autoUpdater.on('checking-for-update', (event, arg) => {
    //
    // })

    // 发现可更新版本时触发
    autoUpdater.on('update-available', (info) => {

        //发现可更新版本-弹层询问渲染进程是否需要“立即更新”
        mainWindow.webContents.send(IPC.UPDATE_AVAILABLE, info);
    })

    // 没有可更新版本时触发
    // autoUpdater.on('update-not-available', (info) => {
    //     // 通知渲染进程，没有检测到新版本
    // })

    //监听用户点击下载事件
    ipcMain.on(IPC.DOWNLOAD_UPDATE,() => {
        //发现可更新版本后-用户操作“立即更新”，此时触发开始下载更新
        autoUpdater.downloadUpdate().then((path) => {
            updaterLogger.info("开始下载更新，文件存放路径：" + path)
        })
    })

    // 下载监听-下载进度数据(0-100%)
    autoUpdater.on('download-progress', (progressObj) => {
        //通知渲染进程，下载进度条界面UI展示
        const downloadProgress = {
            speed: progressObj.bytesPerSecond,
            percentage: parseInt(progressObj.transferred / progressObj.total)
        }
        mainWindow.webContents.send(IPC.UPDATE_DOWNLOAD_PROGRESS, downloadProgress);
    })

    // 更新包下载完成时触发
    autoUpdater.on('update-downloaded', () => {
        // 执行 重启应用程序并安装更新（只能在update-downloaded发出后调用）
        autoUpdater.quitAndInstall()
    })



}

module.exports = checkUpdate;

