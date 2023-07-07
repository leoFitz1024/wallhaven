// Modules to control application life and create native browser window
const {app, Tray, Menu, BrowserWindow} = require('electron')
const path = require('path')
const LOGGER = require('./logger');
const Wallhaven = require('./wallhaven');
const onAutoUpdate = require('./updater');

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
//获取单例锁
const gotTheLock = app.requestSingleInstanceLock()

if (!gotTheLock) {
    app.quit()
} else {
    try {
        app.whenReady().then(() => {
            createWindow()
            app.on('activate', function () {
                // On macOS it's common to re-create a window in the app when the
                // dock icon is clicked and there are no other windows open.
                if (BrowserWindow.getAllWindows().length === 0) createWindow()
            })
        })

        app.on('window-all-closed', function () {
            if (process.platform !== 'darwin') app.quit()
        })

        app.on('quit', () => {
            app.releaseSingleInstanceLock();//释放所有的单例锁
        });
    } catch (error) {
        LOGGER.error(error)
    }
}


function createWindow() {
    // Create the browser window.
    Menu.setApplicationMenu(null)
    const mainWindow = new BrowserWindow({
        width: 1550,
        height: 840,
        show:false,
        frame: false,
        webPreferences: {
            nodeIntegration: true,
            // contextIsolation:false,//允许渲染进程使用nodejs
            preload: path.join(__dirname, 'preload.js')
        }
    })
    LOGGER.debug("启动参数：\r\n" + process.argv)
    let wallhaven = new Wallhaven(mainWindow);
    onAutoUpdate(app, mainWindow)
    wallhaven.init()
    setTray(mainWindow, wallhaven)
    // and load the index.html of the app.
    if(process.argv.indexOf("--autoStart") > -1){
        mainWindow.hide()
    }else{
        mainWindow.show()
    }
    if (app.isPackaged) {
        mainWindow.loadFile('dist/index.html')
    } else {
        mainWindow.loadFile("dist/index.html")
        mainWindow.webContents.openDevTools()
    }
    //修改通知默认签名：electron.app.xx
    app.setAppUserModelId("Wallhaven");
    app.on("child-process-gone", function () {
        wallhaven.close()
    })

    app.on("render-process-gone", function () {
        wallhaven.close()
    })

    app.on('second-instance', (event, commandLine, workingDirectory) => {
        // 当运行第二个实例时,将会聚焦到myWindow这个窗口
        if (mainWindow) {
            if (mainWindow.isMinimized()) {
                mainWindow.restore()
            }else{
                mainWindow.show()
            }
        }
    })


    app.on('quit', () => {
        app.releaseSingleInstanceLock();//释放所有的单例锁
    });
}

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.
// 隐藏主窗口，并创建托盘
function setTray(mainWindow, wallhaven) {
    // 当托盘最小化时，右击有一个菜单显示，这里进设置一个退出的菜单
    let trayMenuTemplate = [
        { // 系统托盘图标目录
            label: '上一张',
            click: function () {
                wallhaven.lastBg();
            }
        }, { // 系统托盘图标目录
            label: '下一张',
            click: function () {
                wallhaven.nextBg();
            }
        }, { // 系统托盘图标目录
            label: '退出',
            click: function () {
                wallhaven.close()
                mainWindow.close(); // 点击之后退出应用
            }
        }];
    // 创建托盘实例
    let iconPath = path.join(__dirname, 'logo.ico');
    let appTray = new Tray(iconPath);
    // 图标的上下文菜单
    const contextMenu = Menu.buildFromTemplate(trayMenuTemplate);

    // 设置托盘悬浮提示
    appTray.setToolTip('wallhaven 3.0');
    // 设置托盘菜单
    appTray.setContextMenu(contextMenu);
    // 单机托盘小图标显示应用
    appTray.on('click', function () {
        // 显示主程序
        mainWindow.show();
    });
}
