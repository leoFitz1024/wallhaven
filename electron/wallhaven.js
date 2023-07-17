const {screen, app, ipcMain, session, Notification, shell, DownloadItem, dialog} = require('electron');
const APP_IPC = require('./common/appIPC.cjs');
const DOWNLOAD_IPC = require('./common/downloadIPC.cjs');
const LOGGER = require('./logger');
const imageSizeof = require('image-size');
const ffi = require('ffi-napi')
const iconv = require('iconv-lite')
const fs = require('fs');
const regUtils = require('./libs/regUtils');
const WallhavenApi = require('./libs/wallhavenApi');
const path = require("path");

const user32 = ffi.Library('user32.dll', {
    SystemParametersInfoA: ['bool', ['uint', 'uint', 'string', 'uint']]
})

const COLOR_REG = /rgb\((.*)\)/;

const BG_MODEL = [[10, 0], [6, 0], [2, 0], [0, 1], [0, 0], [22, 0]]

/**
 填充
 适应
 拉伸
 平铺
 居中
 跨区
 */

const IMG_FILE_TYPE = ["png", "jpeg", "jpg", "bmp", "gif"]

const TH_PREFIX = "https://th.wallhaven.cc/small/"

class Wallhaven {
    constructor(mainWin) {
        this.mainWin = mainWin;
        this.currentBgUrl = "";
        this.currentBgPath = "";
        //定时器id
        this.schedulerId = null;
        this.localStorage = {};
        this.downloadList = {};
        this.pageData = []
        //本地壁纸数据
        this.localBgData = []
        this.wallhavenApi = new WallhavenApi(mainWin)
    }

    init() {
        let that = this
        //启动，加载参数进内存
        ipcMain.on(APP_IPC.START, function (event, data = {}) {
            LOGGER.debug("启动软件参数:" + data)
            let replyData = that.start(data);
            event.reply(APP_IPC.START, replyData)
        })

        //获取本地数据
        ipcMain.on(APP_IPC.GET_DOWNLOADED_IMG, function (event, data = {}) {
            LOGGER.debug("获取本地数据:" + JSON.stringify(data))
            let {page, size} = data
            const localData = that.getLocalData(page, size);
            event.reply(APP_IPC.GET_DOWNLOADED_IMG, localData)
        })

        //更新页面参数
        ipcMain.on(APP_IPC.UPDATE_PAGE_PARAMS, function (event, data = {}) {
            LOGGER.debug("更新页面参数:" + JSON.stringify(data))
            that.updatePageParams(data).then(r => {
                event.reply(APP_IPC.UPDATE_PAGE_PARAMS, {success: true, type: 'success', msg: '保存成功'})
            });
        })

        //保存设置
        ipcMain.on(APP_IPC.SAVE_CONFIG, function (event, data = {}) {
            LOGGER.debug("保存设置:" + data)
            that.updateConfig(JSON.parse(data));
        })

        //关闭代理
        ipcMain.on(APP_IPC.CLOSE_PROXY, function (event, data = {}) {
            LOGGER.debug("关闭网络代理");
            that.closeProxy();
        })

        //切换壁纸
        ipcMain.on(APP_IPC.CHANGE_BG, function (event, data = {}) {
            LOGGER.debug("下载并切换壁纸:" + JSON.stringify(data))
            let {url} = data
            if (url.startsWith("http")) {
                that.downAndChangeBg(data);
                event.reply(APP_IPC.CHANGE_BG, {success: true, type: 'success', msg: '切换中...'})
            } else {
                fs.access(url, fs.constants.F_OK, err => {
                    if (err) {
                        LOGGER.debug(`check file '${url}' access error:`, err)
                        event.reply(APP_IPC.CHANGE_BG, {success: true, type: 'success', msg: '本地文件不存在'})
                    } else {
                        that.doChangeBg(url);
                        event.reply(APP_IPC.CHANGE_BG, {success: true, type: 'success', msg: '切换中...'})
                    }
                })
            }
        })

        //选择文件夹
        ipcMain.on(APP_IPC.SELECT_FOLDER_DIALOG, function (event, data = {}) {
            let res = dialog.showOpenDialogSync({
                title: '请选择文件夹',
                // 默认打开的路径，比如这里默认打开下载文件夹
                defaultPath: data,
                buttonLabel: '确认',
                // 限制能够选择的文件类型
                filters: [
                    // { name: 'Images', extensions: ['jpg', 'png', 'gif'] },
                    // { name: 'Movies', extensions: ['mkv', 'avi', 'mp4'] },
                    // { name: 'Custom File Type', extensions: ['as'] },
                    // { name: 'All Files', extensions: ['*'] },
                ],
                properties: ['openDirectory'],
                message: '请选择文件夹'
            })
            if (res !== undefined) {
                event.reply(APP_IPC.SELECT_FOLDER_DIALOG, res[0])
            }
        })

        //打开路径
        ipcMain.on(APP_IPC.OPEN_FOLDER, function (event, path = {}) {
            fs.access(path, fs.constants.F_OK, err => {
                if (err) {
                    event.reply(APP_IPC.OPEN_FOLDER, {success: false, type: 'error', msg: '路径不存在！'})
                } else {
                    shell.openPath(path).then(res => {
                        if (res === "") {
                            event.reply(APP_IPC.OPEN_FOLDER, {success: true, type: 'success', msg: 'success'})
                        } else {
                            event.reply(APP_IPC.OPEN_FOLDER, {success: false, type: 'error', msg: 'res'})
                        }
                    })
                }
            })
        })

        //打开文件所在位置
        ipcMain.on(APP_IPC.SHOW_FILE_FOLDER, function (event, path = {}) {
            fs.access(path, fs.constants.F_OK, err => {
                if (err) {
                    event.reply(APP_IPC.SHOW_FILE_FOLDER, {success: false, type: 'error', msg: '文件已被删除！'})
                } else {
                    shell.showItemInFolder(path)
                }
            })
        })

        //删除文件
        ipcMain.on(APP_IPC.DELETE_FILE, function (event, path = {}) {
            LOGGER.debug("删除文件:" + path)
            fs.access(path, fs.constants.F_OK, err => {
                if (err) {
                    event.reply(APP_IPC.DELETE_FILE, {success: false, type: 'error', msg: '文件不存在！'})
                } else {
                    fs.unlinkSync(path);
                    event.reply(APP_IPC.DELETE_FILE, {success: true, type: 'success', msg: '删除成功！'})
                }
            })
        })

        // 下载
        ipcMain.on(DOWNLOAD_IPC.DOWNLOAD_FILE, function (e, data) {
            LOGGER.debug("下载图片:" + JSON.stringify(data))
            let {url} = data
            let fileName = url.substr(url.lastIndexOf("/"))
            let filePath = that.localStorage.downloadDir.endsWith("/") ?
                that.localStorage.downloadDir + fileName :
                that.localStorage.downloadDir + "/" + fileName;
            if (!that.downloadList[url]) {
                fs.access(filePath, fs.constants.F_OK, err => {
                    if (err) {
                        data.progress = 0;
                        data.speed = 0;
                        data.state = 'waiting';
                        data.done = false;
                        that.downloadList[url] = {...data}
                        that.downloadFile(url)
                        e.reply(`${DOWNLOAD_IPC.DOWNLOAD_FILE}-${url}`, {
                            success: true,
                            type: 'success',
                            msg: '已加入下载列表'
                        })
                    } else {
                        e.reply(`${DOWNLOAD_IPC.DOWNLOAD_FILE}-${url}`, {success: false, type: 'warning', msg: '文件已存在'})
                    }
                })
            } else {
                e.reply(`${DOWNLOAD_IPC.DOWNLOAD_FILE}-${url}`, {success: false, type: 'warning', msg: '文件正在下载中'})
            }
        })

        // 暂停
        ipcMain.on(DOWNLOAD_IPC.DOWNLOAD_FILE_PAUSE, function (e, data) {
            LOGGER.debug("暂停下载：" + JSON.stringify(data))
            let url = data
            let t = that.downloadList[url]
            if (t) {
                t._downloadFileItem.pause()
                e.reply(`${DOWNLOAD_IPC.DOWNLOAD_FILE_PAUSE}-${url}`, {success: true, type: 'success', msg: '已暂停'})
            } else {
                e.reply(`${DOWNLOAD_IPC.DOWNLOAD_FILE_PAUSE}-${url}`, {success: false, type: 'warning', msg: '文件未在下载中'})
            }

        })

        // 断点恢复下载
        ipcMain.on(DOWNLOAD_IPC.RESUME_DOWNLOAD, function (e, data) {
            LOGGER.debug("继续下载：" + data)
            data = JSON.parse(data)
            let {url} = data
            let t = that.downloadList[url]
            if (t) {
                t._downloadFileItem.resume()
            } else {
                that.downloadList[url] = {...data}
                that.resumeDownload(data)
            }
            e.reply(`${DOWNLOAD_IPC.RESUME_DOWNLOAD}-url`, '已恢复下载')
        })

        // 取消下载
        ipcMain.on(DOWNLOAD_IPC.DOWNLOAD_CANCEL, function (e, data) {
            LOGGER.debug("取消下载：" + JSON.stringify(data))
            let url = data
            let t = that.downloadList[url]
            if (t) {
                t._downloadFileItem.cancel()
                e.reply(`${DOWNLOAD_IPC.DOWNLOAD_CANCEL}-${url}`, {success: true, type: 'success', msg: '已取消下载'})
            } else {
                e.reply(`${DOWNLOAD_IPC.DOWNLOAD_CANCEL}-${url}`, {success: false, type: 'error', msg: '文件未在下载中'})
                // 删除未下在完成文件
            }
        })

        // 打开调试
        ipcMain.on("toggle_dev_tools", function (event, arg) {
            that.mainWin.webContents.toggleDevTools();
        })

        //清除数据
        ipcMain.on(APP_IPC.CLEAR_DATA, function () {
            LOGGER.debug("清除应用数据。")
            const clearObj = {
                storages: ['appcache', 'filesystem', 'localstorage', 'shadercache', 'websql', 'serviceworkers', 'cachestorage'],
            };
            //在主进程里面调用示例代码
            if (that.mainWin) {
                that.mainWin.webContents.session.clearStorageData(clearObj).then(res => {
                    app.relaunch()
                    app.exit(0)
                })
            }
        })

        // 重启
        ipcMain.on(APP_IPC.RESTART, function () {
            app.relaunch();
            app.exit(0)
        })

        // 最小化
        ipcMain.on(APP_IPC.MIN_WINDOW, function () {
            that.mainWin.minimize()
        })

        // 最大化
        ipcMain.on(APP_IPC.MAX_WINDOW, function () {
            if (that.mainWin.isMaximized()) {
                that.mainWin.unmaximize()
            } else {
                that.mainWin.maximize()
            }
        })

        // 关闭程序
        ipcMain.on(APP_IPC.CLOSE_WINDOW, function () {
            LOGGER.debug("最小化到托盘.")
            that.mainWin.hide();
            new Notification({
                title: "提示",
                body: "Wallhaven已最小化到托盘",
                icon: path.join(__dirname, 'app.png')
            }).show();
        })

        ipcMain.on(APP_IPC.OPEN_LINK, (event, url) => {
            shell.openExternal(url);
        })

        // 监听下载
        session.defaultSession.on('will-download', (e, item) => {
            try {
                const url = item.getURL()
                let downloadItem = that.downloadList[url] || {
                    notSend: true
                };
                // 获取文件的总大小
                const totalBytes = item.getTotalBytes();
                // 设置下载路径
                const filePath = path.join(app.getPath("downloads"), item.getFilename());
                item.setSavePath(filePath);

                //缓存downitem
                downloadItem._downloadFileItem = item;
                downloadItem.path = item.getSavePath();
                downloadItem.eTag = item.getETag();
                downloadItem.urlChain = item.getURLChain();
                downloadItem.size = totalBytes
                downloadItem.lastModified = item.getLastModifiedTime()
                downloadItem.startTime = item.getStartTime();

                // 监听下载过程，计算并设置进度条进度
                let lastBytes = 0;
                item.on('updated', (event, state) => {
                    if (state === 'interrupted') {
                        downloadItem.state = 'interrupted'
                    } else if (state === 'progressing') {
                        if (item.isPaused()) {
                            downloadItem.state = 'paused'
                        } else {
                            let offset = item.getReceivedBytes();
                            downloadItem.state = 'downloading';
                            downloadItem.speed = offset - lastBytes;
                            downloadItem.progress = parseInt((offset / totalBytes) * 100);
                            lastBytes = offset
                            downloadItem.offset = offset
                        }
                    }
                    !downloadItem.notSend && that.mainWin.webContents.send(DOWNLOAD_IPC.UPDATE_DOWNLOAD_STATE, JSON.parse(JSON.stringify(downloadItem)));
                })

                // 下载完成
                item.once('done', (event, state) => {
                    downloadItem.done = true
                    switch (state) {
                        case 'interrupted':
                            downloadItem.state = 'interrupted-err'
                            break;
                        case 'cancelled':
                            downloadItem.state = 'cancelled'
                            break;
                        default:
                            downloadItem.state = 'completed'
                            that.notification(downloadItem.path)
                            break;
                    }
                    if (downloadItem.state !== 'cancelled') {
                        !downloadItem.notSend && that.mainWin.webContents.send(DOWNLOAD_IPC.UPDATE_DOWNLOAD_STATE, JSON.parse(JSON.stringify(downloadItem)))
                        if (state === "completed") {
                            this.notifyChangeBg(url)
                        }
                    }
                    //删除缓存
                    delete that.downloadList[url]
                    downloadItem = null;
                    item = null;
                })

                // 恢复
                if (item.canResume) {
                    item.resume()
                }

            } catch (error) {
                LOGGER.error("download error:", error)
            }
        })

    }

    /**
     * 启动时从页面将数据读进内存，并初始化部分数据
     * @param data
     */
    start(data) {
        this.localStorage = JSON.parse(data);
        if (this.localStorage.downloadDir === "") {
            this.localStorage.downloadDir = app.getPath("downloads")
        } else {
            app.setPath("downloads", this.localStorage.downloadDir)
        }
        let {width, height} = screen.getPrimaryDisplay().size;//获取到屏幕的宽度和高度
        let response = {
            "downloads": this.localStorage.downloadDir,
            "desktopInfo": width + " x " + height
        }
        this.initImagesDir()
        this.updatePageData().then(r => {
            this.loadScheduler()
        })
        this.loadAutoStart()
        this.setProxy()
        this.loadLocalData()
        return JSON.stringify(response)
    }

    getLocalData(page, size) {
        this.loadLocalData();
        let data;
        const start = (page - 1) * size
        const end = Math.min(start + size, this.localBgData.length)
        if (start < this.localBgData.length) {
            data = []
            for (let i = start; i < end; i++) {
                const item = this.localBgData[i];
                if (item.id.indexOf("wallhaven-") > -1) {
                    let id = item.id.replace("wallhaven-", "");
                    id = id.substr(0, id.indexOf("."))
                    const hChar = id.substr(0, 2)
                    item.src = `${TH_PREFIX}${hChar}/${id}.jpg`
                }
                item.base64 = this.base64Encode(item.path)
                data.push(item)
            }
        } else {
            data = []
        }

        const totalPage = Math.ceil(this.localBgData.length / size)
        return {
            'currentPage': page,
            'totalPage': totalPage,
            'data': data
        }
    }

    /**
     * 加载本地数据
     */
    loadLocalData() {
        let dirPath = this.localStorage.downloadDir;
        let that = this;
        this.localBgData.length = 0
        const files = fs.readdirSync(dirPath);
        //遍历读取到的文件列表
        files.forEach(function (fileName) {
            //获取当前文件的绝对路径
            let curPath = path.join(dirPath, fileName);
            let isImg = false
            let fileType = ""
            if (fileName.indexOf(".") > -1) {
                fileType = fileName.split(".")[1]
                if (IMG_FILE_TYPE.indexOf(fileType) > -1) {
                    isImg = true
                }
            }
            if (isImg) {
                //根据文件路径获取文件信息，返回一个fs.Stats对象
                const stats = fs.statSync(curPath);
                if (stats.isFile() && stats.size > 0) {
                    try {
                        const imageSize = imageSizeof(curPath);
                        const item = {
                            "id": fileName,
                            "path": curPath,
                            "resolution": `${imageSize.width} x ${imageSize.height}`,
                            "file_size": stats.size,
                            "file_type": fileType,
                            "ctime": stats.ctime.getTime()
                        }
                        that.localBgData.push(item)
                    } catch (e) {
                        // LOGGER.error(e)
                    }
                }
            }
        });
        that.localBgData.sort((a, b) => {
            return b.ctime - a.ctime;
        })
    }

    /**
     * 加载定时器
     */
    loadScheduler() {
        if (this.schedulerId !== null) {
            clearInterval(this.schedulerId)
        }
        if (this.localStorage.scheduleTime !== 0) {
            let scheduleTime
            if (this.localStorage.scheduleTime === -1) {
                scheduleTime = this.localStorage.customScheduleTime
            } else {
                scheduleTime = this.localStorage.scheduleTime
            }
            LOGGER.debug(`已开启定时切换，间隔：${scheduleTime}分钟`)
            let scheduleMills = scheduleTime * 60000
            this.schedulerId = setInterval(() => {
                this.nextBg()
            }, scheduleMills)
        } else {
            LOGGER.debug(`已关闭定时切换。`)
        }
    }

    /**
     * 加载是否开机自启
     */
    loadAutoStart() {
        // 获取可执行文件位置
        if (this.localStorage.autoStart === 0) {
            // 关闭 开机自启动
            LOGGER.debug("开机自启：OFF")
            app.setLoginItemSettings({
                openAtLogin: false,
            });
        } else {
            // 打开 开机自启动
            LOGGER.debug("开机自启：ON")
            app.setLoginItemSettings({
                openAtLogin: true,
                openAsHidden: true,
                args: ["--autoStart"]
            });
        }
    }

    /**
     * 设置网络代理
     */
    setProxy(proxy) {
        if (proxy === undefined) {
            proxy = this.localStorage.proxy
        }
        LOGGER.info(`网络代理参数：开启：${proxy.enable}, 协议: ${proxy.protocol}, 地址: ${proxy.address}, 端口: ${proxy.port}`);
        this.localStorage.proxy = proxy;
        if (proxy.enable !== true || proxy.address === "" || proxy.port === "") {
            LOGGER.info("关闭网络代理");
            this.mainWin.webContents.session.setProxy({mode: "direct"});
        } else {
            LOGGER.info("开启网络代理");
            this.mainWin.webContents.session.setProxy({
                mode: "fixed_servers",
                proxyRules: proxy.protocol + "://" + proxy.address + ":" + proxy.port
            });
        }
    }

    /**
     * 关闭代理
     */
    closeProxy() {
        this.mainWin.webContents.session.setProxy({mode: "direct"});
    }

    /**
     * 关闭
     */
    close() {
        LOGGER.info(`关闭程序，保存数据。`)
        if (this.schedulerId !== null) {
            clearInterval(this.schedulerId)
        }
        for (let key in this.downloadList) {
            if (this.downloadList.hasOwnProperty(key)) {
                let element = this.downloadList[key];
                if (element._downloadFileItem) {
                    element._downloadFileItem.pause()
                    element._downloadFileItem = null
                }
            }
        }
    }

    /**
     * 初始化下载文件夹
     */
    initImagesDir() {
        if (!fs.existsSync(this.localStorage.downloadDir)) {
            fs.mkdirSync(this.localStorage.downloadDir)
            LOGGER.debug(`文件夹：${this.localStorage.downloadDir} 不存在，已自动创建。`)
        }
    }

    /**
     * 更新页面参数
     */
    updatePageParams(data) {
        this.localStorage.apiParams = data;
        this.localStorage.pageIndex = 0
        this.localStorage.currentPage = 1
        return this.updatePageData()
    }

    /**
     * 更新配置
     */
    updateConfig(data) {
        let that = this
        this.setProxy(data.proxy)
        that.localStorage.scheduleTime = data.scheduleTime;
        that.localStorage.customScheduleTime = data.customScheduleTime;
        that.loadScheduler()
        that.localStorage.downloadDir = data.downloadDir;
        app.setPath("downloads", data.downloadDir)
        that.localStorage.switchModel = data.switchModel;
        that.localStorage.autoStart = data.autoStart;
        this.loadAutoStart()
        if ((that.localStorage.fullModel !== data.fullModel)
            || (that.localStorage.bgColor !== data.bgColor)) {
            that.localStorage.fullModel = data.fullModel;
            that.localStorage.bgColor = data.bgColor;
            this.refreshBg()
        }
        this.mainWin.webContents.send(APP_IPC.SAVE_CONFIG, {success: true, type: 'success', msg: "保存成功"})
    }

    /**
     * 更新内存里页面数据
     */
    async updatePageData() {
        await this.wallhavenApi.search(`${this.localStorage.apiParams}&page=${this.localStorage.currentPage}`,
            (data) => {
                if (data) {
                    LOGGER.info("更新内存数据成功")
                    if (this.localStorage.totalPage > data['meta']['last_page']) {
                        this.localStorage.currentPage = 1
                        this.localStorage.totalPage = data['meta']['last_page']
                        this.updatePageData()
                    } else {
                        this.localStorage.totalPage = data['meta']['last_page']
                        this.pageData.length = 0
                        for (let i in data['data']) {
                            let imgItem = data['data'][i]
                            let item = {
                                "id": imgItem.id,
                                'url': imgItem['path'],
                                "size": imgItem['file_size'],
                                'colors': imgItem['colors'],
                                'small': imgItem['thumbs']['small'],
                                'resolution': imgItem['resolution']
                            }
                            this.pageData.push(item)
                        }
                    }
                } else {
                    LOGGER.error("更新内存数据失败")
                }
            })
    }

    /**
     * 上一张
     */
    lastBg() {
        if (this.localStorage.switchModel === 'online') {
            if ((0 < this.localStorage.pageIndex && this.localStorage.pageIndex < this.pageData.length) || (
                this.localStorage.currentPage > 1)) {
                if (0 < this.localStorage.pageIndex < this.pageData.length) {
                    this.localStorage.pageIndex--;
                    this.downAndChangeBg(this.pageData[this.localStorage.pageIndex])
                } else {
                    this.localStorage.pageIndex = 0
                    this.localStorage.currentPage--
                    this.updatePageData().then(r => {
                        this.downAndChangeBg(this.pageData[this.localStorage.pageIndex])
                    })
                }
            } else {
                this.localStorage.currentPage = this.localStorage.totalPage
                this.updatePageData().then(r => {
                    this.localStorage.pageIndex = this.pageData.length - 1
                    this.downAndChangeBg(this.pageData[this.localStorage.pageIndex])
                })
            }
        } else {
            this.loadLocalData()
            if (this.localBgData.length > 0) {
                if (this.localStorage.local_bg_index > 0) {
                    this.localStorage.local_bg_index--
                } else {
                    this.localStorage.local_bg_index = this.localBgData.length - 1
                }
                this.doLocalChange()
            }
        }
    }

    /**
     * 下一张
     */
    nextBg() {
        if (this.localStorage.switchModel === 'online') {
            if ((this.localStorage.pageIndex < this.pageData.length - 1) || (
                this.localStorage.currentPage < this.localStorage.totalPage)) {
                if (this.localStorage.pageIndex < this.pageData.length - 1) {
                    this.localStorage.pageIndex++
                    this.downAndChangeBg(this.pageData[this.localStorage.pageIndex])
                } else {
                    this.localStorage.pageIndex = 0
                    this.localStorage.currentPage++
                    this.updatePageData().then(r => {
                        this.downAndChangeBg(this.pageData[this.localStorage.pageIndex])
                    })
                }
            } else {
                this.localStorage.currentPage = 1
                this.localStorage.pageIndex = 0
                this.updatePageData().then(r => {
                    console.log(r)
                    this.downAndChangeBg(this.pageData[this.localStorage.pageIndex])
                })
            }
        } else {
            this.loadLocalData()
            if (this.localBgData.length > 0) {
                if (this.localStorage.local_bg_index < this.localBgData.length - 1) {
                    this.localStorage.local_bg_index++
                } else {
                    this.localStorage.local_bg_index = 0
                }
                this.doLocalChange()
            }
        }
    }

    /**
     * 下载完成，通知切换
     */
    notifyChangeBg(url) {
        if (url === this.currentBgUrl) {
            let fileName = url.substr(url.lastIndexOf("/"))
            let filePath = path.join(this.localStorage.downloadDir, fileName)
            this.doChangeBg(filePath)
        }
    }

    /**
     * 执行切换壁纸操作
     */
    doChangeBg(path) {
        LOGGER.info("切换壁纸：" + path)
        let bgColorStr = COLOR_REG.exec(this.localStorage.bgColor)[1].trim().split(",").join("")
        let model = this.localStorage.fullModel
        regUtils.addKey("HKEY_CURRENT_USER\\Control Panel\\Desktop", "WallpaperStyle", BG_MODEL[model][0]).then(r => {
            regUtils.addKey("HKEY_CURRENT_USER\\Control Panel\\Desktop", "TileWallpaper", BG_MODEL[model][1]).then(r => {
                // regUtils.addKey("HKEY_CURRENT_USER\\Control Panel\\Desktop", "WallPaper", path).then(res => {
                regUtils.addKey("HKEY_CURRENT_USER\\Control Panel\\Colors", "Background", bgColorStr).then(res => {
                    const pathBuf = iconv.encode(path, "gbk");
                    const systemParametersInfoA = user32.SystemParametersInfoA(20, 0, pathBuf, 1);
                    this.currentBgPath = path
                    LOGGER.info("切换成功：" + path)
                })
                // })
            })
        })
    }

    /**
     * 刷新一下壁纸
     */
    refreshBg() {
        this.doChangeBg(this.currentBgPath)
    }

    /**
     * 本地切换
     */
    doLocalChange() {
        const bgPath = this.localBgData[this.localStorage.local_bg_index].path;
        this.doChangeBg(bgPath);
    }

    /**
     * 下载壁纸,然后切换
     * @param data
     */
    downAndChangeBg(data) {
        if (data) {
            let {url} = data
            this.currentBgUrl = url
            let fileName = url.substr(url.lastIndexOf("/"))
            let filePath = this.localStorage.downloadDir.endsWith("/") ?
                this.localStorage.downloadDir + fileName :
                this.localStorage.downloadDir + "/" + fileName;
            if (!this.downloadList[url]) {
                fs.access(filePath, fs.constants.F_OK, err => {
                    if (err) {
                        this.downloadList[url] = {...data}
                        this.downloadFile(url)
                    } else {
                        this.notifyChangeBg(url)
                    }
                })
            }
        } else {
            LOGGER.error("切换壁纸失败：data is undefined.")
        }
    }

    /**
     * 下载文件
     * @param url
     */
    downloadFile(url) {
        session.defaultSession.downloadURL(url)
    }

    // 恢复下载
    resumeDownload = (obj = {}) => {
        let {path = '', urlChain = [], offset = 0, size = 0, lastModified, eTag, startTime} = obj;
        if (!path || urlChain.length === 0 || size === 0) {
            return;
        }
        session.defaultSession.createInterruptedDownload({
            path, urlChain, offset, length: size, lastModified, eTag, startTime
        })
    }

    notification = (url) => {
        // let noti = new Notification({
        //     title: "下载成功",
        //     bodyString: url,
        //     silentBoolean: false,
        //     icon: url
        // })
        // noti.show()
        // noti.once("click", () => {
        //     shell.showItemInFolder(url)
        // })
    }

    /**
     * 文件转base64
     */
    base64Encode = file => {
        let bitmap = fs.readFileSync(file);
        let fileType = file.split(".")[1]
        if ("jpg" === fileType) {
            fileType = "jpeg"
        }
        return `data:image/${fileType};base64,${Buffer.from(bitmap).toString('base64')}`;
    }
}

module.exports = Wallhaven;
