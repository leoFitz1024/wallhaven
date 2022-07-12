const {screen, app, ipcMain, session, Notification, shell, DownloadItem, dialog} = require('electron');
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
        this.wallhavenApi = new WallhavenApi()
    }

    init() {
        let that = this
        //启动，加载参数进内存
        ipcMain.on("start", function (event, data = {}) {
            LOGGER.debug("start,load localStorage data:" + JSON.stringify(data))
            let replyData = that.start(data);
            event.reply('start', replyData)
        })

        //获取本地数据
        ipcMain.on("get-local-data", function (event, data = {}) {
            LOGGER.debug("receive 'get-local-data':" + JSON.stringify(data))
            let {page, size} = data
            const localData = that.getLocalData(page, size);
            event.reply('get-local-data-receive', localData)
        })

        //更新页面参数
        ipcMain.on("update-page-params", function (event, data = {}) {
            LOGGER.debug("receive 'update-page-params':" + JSON.stringify(data))
            that.updatePageParams(data).then(r => {
                event.reply("update-page-params-receive", {success: true, type: 'success', msg: '保存成功'})
            });
        })

        //保存设置
        ipcMain.on("update-config", function (event, data = {}) {
            LOGGER.debug("receive 'update-config':" + JSON.stringify(data))
            that.updateConfig(data);
        })

        //选择文件夹
        ipcMain.on("show-open-dialog-sync", function (event, data = {}) {
            LOGGER.debug("receive 'show-open-dialog-sync':" + JSON.stringify(data))
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
                event.reply("show-open-dialog-receive", res[0])
            }
        })

        //打开路径
        ipcMain.on("open-folder", function (event, path = {}) {
            LOGGER.debug("receive 'open-folder':" + path)
            fs.access(path, fs.constants.F_OK, err => {
                if (err) {
                    event.reply("open-folder-receive", {success: false, type: 'error', msg: '路径不存在！'})
                } else {
                    shell.openPath(path).then(res => {
                        if (res === "") {
                            event.reply("open-folder-receive", {success: true, type: 'success', msg: 'success'})
                        } else {
                            event.reply("open-folder-receive", {success: false, type: 'error', msg: 'res'})
                        }
                    })
                }
            })
        })

        //打开文件所在位置
        ipcMain.on("show-item-in-folder", function (event, path = {}) {
            LOGGER.debug("receive 'show-item-in-folder':" + path)
            fs.access(path, fs.constants.F_OK, err => {
                if (err) {
                    event.reply("show-item-in-folder-receive", {success: false, type: 'error', msg: '文件已被删除！'})
                } else {
                    shell.showItemInFolder(path)
                }
            })
        })

        //打开文件所在位置
        ipcMain.on("delete-file", function (event, path = {}) {
            LOGGER.debug("receive 'delete-file':" + path)
            fs.access(path, fs.constants.F_OK, err => {
                if (err) {
                    event.reply("delete-file-receive", {success: false, type: 'error', msg: '文件不存在！'})
                } else {
                    fs.unlinkSync(path);
                    event.reply("delete-file-receive", {success: true, type: 'success', msg: '删除成功！'})
                }
            })
        })


        //切换壁纸
        ipcMain.on("change-bg", function (event, data = {}) {
            LOGGER.debug("receive 'change-bg':" + JSON.stringify(data))
            let {url} = data
            if (url.startsWith("http")) {
                that.downAndChangeBg(data);
                event.reply("change-bg-receive", {success: true, type: 'success', msg: '切换中...'})
            } else {
                fs.access(url, fs.constants.F_OK, err => {
                    if (err) {
                        LOGGER.debug(`check file '${url}' access error:`, err)
                        event.reply("change-bg-receive", {success: true, type: 'success', msg: '本地文件不存在'})
                    } else {
                        that.doChangeBg(url);
                        event.reply("change-bg-receive", {success: true, type: 'success', msg: '切换中...'})
                    }
                })
            }
        })

        // 下载
        ipcMain.on("download-file", function (e, data) {
            LOGGER.debug("receive 'download-file':" + JSON.stringify(data))
            let {url} = data
            let fileName = url.substr(url.lastIndexOf("/"))
            let filePath = that.localStorage['download_dir'].endsWith("/") ?
                that.localStorage['download_dir'] + fileName :
                that.localStorage['download_dir'] + "/" + fileName;
            if (!that.downloadList[url]) {
                fs.access(filePath, fs.constants.F_OK, err => {
                    if (err) {
                        data.progress = 0;
                        data.speed = 0;
                        data.state = 'waiting';
                        data.done = false;
                        that.downloadList[url] = {...data}
                        that.downloadFile(url)
                        e.reply("download-file-" + url, {success: true, type: 'success', msg: '已加入下载列表'})
                    } else {
                        e.reply("download-file-" + url, {success: false, type: 'warning', msg: '文件已存在'})
                    }
                })
            } else {
                e.reply("download-file-" + url, {success: false, type: 'warning', msg: '文件正在下载中'})
            }
        })

        // 暂停
        ipcMain.on("download-file-pause", function (e, data) {
            LOGGER.debug("receive 'download-file-pause':" + JSON.stringify(data))
            let url = data
            let t = that.downloadList[url]
            if (t) {
                t._downloadFileItem.pause()
                e.reply("download-file-pause-" + url, {success: true, type: 'success', msg: '已暂停'})
            } else {
                e.reply("download-file-pause-" + url, {success: false, type: 'warning', msg: '文件未在下载中'})
            }

        })

        // 断点恢复下载
        ipcMain.on("resume-download", function (e, data) {
            LOGGER.debug("receive 'resume-download':" + data)
            data = JSON.parse(data)
            let {url} = data
            let t = that.downloadList[url]
            if (t) {
                t._downloadFileItem.resume()
            } else {
                that.downloadList[url] = {...data}
                that.resumeDownload(data)
            }
            e.reply("download-file-resume-" + url, '已恢复下载')
        })

        // 继续
        //未用到
        ipcMain.on("download-file-resume", function (e, data) {
            LOGGER.debug("receive 'download-file-resume':" + JSON.stringify(data))
            let {url} = data
            let t = that.downloadList[url]
            if (t) {
                t._downloadFileItem.resume()
                e.reply("download-file-resume-" + url, {success: true, type: 'success', msg: '已恢复下载'})
            }

        })

        // 取消下载
        ipcMain.on("download-file-cancel", function (e, data) {
            LOGGER.debug("receive 'download-file-cancel':" + JSON.stringify(data))
            let url = data
            let t = that.downloadList[url]
            if (t) {
                t._downloadFileItem.cancel()
                e.reply("download-file-cancel-" + url, {success: true, type: 'success', msg: '已取消下载'})
            } else {
                e.reply("download-file-cancel-" + url, {success: false, type: 'error', msg: '文件未在下载中'})
                // 删除未下在完成文件
            }
        })

        // 打开调试
        ipcMain.on("toggle_dev_tools", function (event, arg) {
            that.mainWin.webContents.toggleDevTools();
        })

        // 重启
        ipcMain.on("clear-data", function () {
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
        ipcMain.on("restart", function () {
            app.relaunch();
            app.exit(0)
        })

        // 最小化
        ipcMain.on("min", function () {
            that.mainWin.minimize()
        })

        // 最大化
        ipcMain.on("max", function () {
            if (that.mainWin.isMaximized()) {
                that.mainWin.unmaximize()
            } else {
                that.mainWin.maximize()
            }
        })

        // 关闭程序
        ipcMain.on("close", function () {
            LOGGER.debug("最小化到托盘.")
            that.mainWin.hide();
            new Notification({
                title: "提示",
                body: "Wallhaven已最小化到托盘",
                icon: path.join(__dirname, 'app.png')
            }).show();
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
                    !downloadItem.notSend && that.mainWin.webContents.send("update-download-state", JSON.parse(JSON.stringify(downloadItem)));
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
                        !downloadItem.notSend && that.mainWin.webContents.send("update-download-state", JSON.parse(JSON.stringify(downloadItem)))
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
        if (this.localStorage['api_key'] !== null && this.localStorage['api_key'] !== '') {
            this.wallhavenApi.setApikey(this.localStorage['api_key'])
        }
        if (this.localStorage['download_dir'] === "") {
            this.localStorage['download_dir'] = app.getPath("downloads")
        } else {
            app.setPath("downloads", this.localStorage['download_dir'])
        }
        let {width, height} = screen.getPrimaryDisplay().size;//获取到屏幕的宽度和高度
        let response = {
            "downloads": this.localStorage['download_dir'],
            "desktopInfo": width + " x " + height
        }
        this.initImagesDir()
        this.updatePageData().then(r => {
            this.loadScheduler()
        })
        this.loadAutoStart()
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
        const response = {
            'current_page': page,
            'total_page': totalPage,
            'data': data
        }
        return response
    }

    /**
     * 加载本地数据
     */
    loadLocalData() {
        let dirPath = this.localStorage['download_dir'];
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
                    }catch (e){
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
        if (this.localStorage['schedule_time'] !== 0) {
            let scheduleTime
            if(this.localStorage['schedule_time'] === -1){
                scheduleTime = this.localStorage['custom_schedule_time']
            }else{
                scheduleTime = this.localStorage['schedule_time']
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
        if (this.localStorage['auto_start'] === 0) {
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
        if (!fs.existsSync(this.localStorage['download_dir'])) {
            fs.mkdirSync(this.localStorage['download_dir'])
            LOGGER.debug(`文件夹：${this.localStorage['download_dir']} 不存在，已自动创建。`)
        }
    }

    /**
     * 更新页面参数
     */
    updatePageParams(data) {
        this.localStorage['api_params'] = data;
        this.localStorage['page_index'] = 0
        this.localStorage['current_page'] = 1
        return this.updatePageData()
    }

    /**
     * 更新配置
     */
    updateConfig(data) {
        let that = this
        this.wallhavenApi.checkApiKey(data['api_key']).then(res => {
            let setKeySuccess = true;
            if (res) {
                LOGGER.info("set apiKey success: " + data['api_key'])
                that.localStorage['api_key'] = data['api_key'];
                that.wallhavenApi.setApikey(data['api_key'])
            } else {
                if (data['api_key'] !== "") {
                    LOGGER.info("set apiKey error: " + data['api_key'])
                    that.localStorage['api_key'] = "";
                    that.wallhavenApi.setApikey(null)
                    setKeySuccess = false
                }
            }
            that.localStorage['schedule_time'] = data['schedule_time'];
            that.localStorage['custom_schedule_time'] = data['custom_schedule_time'];
            that.loadScheduler()
            that.localStorage['download_dir'] = data['download_dir'];
            app.setPath("downloads", data['download_dir'])
            that.localStorage['switch_model'] = data['switch_model'];
            that.localStorage['auto_start'] = data['auto_start'];
            this.loadAutoStart()
            if (setKeySuccess === true) {
                that.mainWin.webContents.send("update-config-receive", {success: true, type: 'success', msg: "保存成功"})
            } else {
                that.mainWin.webContents.send("update-config-receive", {
                    success: false,
                    type: 'warning',
                    msg: "apKey 无效，已重置"
                })
            }
            if((that.localStorage['full_model'] !== data['full_model'])
                || (that.localStorage['bg_color'] !== data['bg_color'])){
                that.localStorage['full_model'] = data['full_model'];
                that.localStorage['bg_color'] = data['bg_color'];
                this.refreshBg()
            }
        })
    }

    /**
     * 更新内存里页面数据
     */
    async updatePageData() {
        await this.wallhavenApi.request(this.localStorage['api_params'], this.localStorage['current_page']).then(res => {
            let data = res.data
            if (this.localStorage['total_page'] > data['meta']['last_page']) {
                this.localStorage['current_page'] = 1
                this.localStorage['total_page'] = data['meta']['last_page']
                this.updatePageData()
            } else {
                this.localStorage['total_page'] = data['meta']['last_page']
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
        }).catch(err => {
            console.log(err)
        })
    }

    /**
     * 上一张
     */
    lastBg() {
        if (this.localStorage['switch_model'] === 'online') {
            if ((0 < this.localStorage['page_index'] && this.localStorage['page_index'] < this.pageData.length) || (
                this.localStorage['current_page'] > 1)) {
                if (0 < this.localStorage['page_index'] < this.pageData.length) {
                    this.localStorage['page_index']--;
                    this.downAndChangeBg(this.pageData[this.localStorage['page_index']])
                } else {
                    this.localStorage['page_index'] = 0
                    this.localStorage['current_page']--
                    this.updatePageData().then(r => {
                        this.downAndChangeBg(this.pageData[this.localStorage['page_index']])
                    })
                }
            } else {
                this.localStorage['current_page'] = this.localStorage['total_page']
                this.updatePageData().then(r => {
                    this.localStorage['page_index'] = this.pageData.length - 1
                    this.downAndChangeBg(this.pageData[this.localStorage['page_index']])
                })
            }
        } else {
            this.loadLocalData()
            if (this.localBgData.length > 0) {
                if (this.localStorage['local_bg_index'] > 0) {
                    this.localStorage['local_bg_index']--
                } else {
                    this.localStorage['local_bg_index'] = this.localBgData.length - 1
                }
                this.doLocalChange()
            }
        }
    }

    /**
     * 下一张
     */
    nextBg() {
        if (this.localStorage['switch_model'] === 'online') {
            if ((this.localStorage['page_index'] < this.pageData.length - 1) || (
                this.localStorage['current_page'] < this.localStorage['total_page'])) {
                if (this.localStorage['page_index'] < this.pageData.length - 1) {
                    this.localStorage['page_index']++
                    this.downAndChangeBg(this.pageData[this.localStorage['page_index']])
                } else {
                    this.localStorage['page_index'] = 0
                    this.localStorage['current_page']++
                    this.updatePageData().then(r => {
                        this.downAndChangeBg(this.pageData[this.localStorage['page_index']])
                    })
                }
            } else {
                this.localStorage['current_page'] = 1
                this.localStorage['page_index'] = 0
                this.updatePageData().then(r => {
                    this.downAndChangeBg(this.pageData[this.localStorage['page_index']])
                })
            }
        } else {
            this.loadLocalData()
            if (this.localBgData.length > 0) {
                if (this.localStorage['local_bg_index'] < this.localBgData.length - 1) {
                    this.localStorage['local_bg_index']++
                } else {
                    this.localStorage['local_bg_index'] = 0
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
            let filePath = path.join(this.localStorage['download_dir'], fileName)
            this.doChangeBg(filePath)
        }
    }

    /**
     * 执行切换壁纸操作
     */
    doChangeBg(path) {
        LOGGER.info("切换壁纸：" + path)
        let bgColorStr = COLOR_REG.exec(this.localStorage['bg_color'])[1].trim().split(",").join("")
        let model = this.localStorage['full_model']
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
    refreshBg(){
        this.doChangeBg(this.currentBgPath)
    }

    /**
     * 本地切换
     */
    doLocalChange() {
        const bgPath = this.localBgData[this.localStorage['local_bg_index']].path;
        this.doChangeBg(bgPath);
    }

    /**
     * 下载壁纸,然后切换
     * @param data
     */
    downAndChangeBg(data) {
        let {url} = data
        this.currentBgUrl = url
        let fileName = url.substr(url.lastIndexOf("/"))
        let filePath = this.localStorage['download_dir'].endsWith("/") ?
            this.localStorage['download_dir'] + fileName :
            this.localStorage['download_dir'] + "/" + fileName;
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
