const {autoUpdater} = require("electron-updater");
const LOGGER = require('./logger');

//监听更新
function onAutoUpdate(app, mainWindow) {
    LOGGER.info("检查更新")
    app.on('ready', function () {
        autoUpdater.checkForUpdatesAndNotify();
    });

    function sendStatusToWindow(text) {
        mainWindow.webContents.send('update-message', text);
    }

    autoUpdater.on('checking-for-update', () => {
        sendStatusToWindow('Checking for update...');
    })

    autoUpdater.on('update-available', (info) => {
        sendStatusToWindow('Update available.');
    })

    autoUpdater.on('update-not-available', (info) => {
        sendStatusToWindow('Update not available.');
    })

    autoUpdater.on('error', (err) => {
        sendStatusToWindow('Error in auto-updater. ' + err);
    })

    autoUpdater.on('download-progress', (progressObj) => {
        let log_message = "Download speed: " + progressObj.bytesPerSecond;
        log_message = log_message + ' - Downloaded ' + progressObj.percent + '%';
        log_message = log_message + ' (' + progressObj.transferred + "/" + progressObj.total + ')';
        sendStatusToWindow(log_message);
    })

    autoUpdater.on('update-downloaded', (info) => {
        sendStatusToWindow('Update downloaded');
    });
}

module.exports = onAutoUpdate;

