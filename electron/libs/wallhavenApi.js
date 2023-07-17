const LOGGER = require("../logger");
const {ipcMain} = require('electron');
const API_IPC = require("../common/apiIPC.cjs");

module.exports = class WallhavenApi {
    constructor(mainWindow) {
        this.mainWindow = mainWindow
    }

    //获取数据
    search(params, callback){
        this.mainWindow.webContents.send(API_IPC.SEARCH, params);
        ipcMain.once(API_IPC.SEARCH, (event,data) => {
            callback(data)
        })
    }
}
