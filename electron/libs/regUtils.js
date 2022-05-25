/**
 * @file 添加、删除注册列表的key值
 */
// eslint-disable-next-line camelcase
const child_process = require('child_process');

//  注意：`HKEY_CURRENT_USER`可以简写为`HKCU`，在网上看到的`HKCU`也就是`HKEY_CURRENT_USER`的意思

// 默认的自启动注册列表地址
const startKeyPath = 'HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\\';

module.exports = {
    deleteKey(keyPath, value) {
        return new Promise((resolve, reject) => {
            try {
                let cmd = `reg delete ${keyPath} /v ${value} /f`
                const result = child_process.exec(cmd);
                resolve(result);
            } catch (error) {
                reject(error);
            }
        });
    },
    addKey(keyPath, name, value) {
        return new Promise((resolve, reject) => {
            try {
                let cmd = `reg add "${keyPath}" /v "${name}" /t REG_SZ /d "${value}" /f`
                const result = child_process.exec(cmd);
                resolve(result);
            } catch (error) {
                reject(error);
            }
        });
    }
}
