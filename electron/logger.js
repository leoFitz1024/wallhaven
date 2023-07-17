const logger = require('electron-log')
const path = require('path')

logger.transports.file.level = 'debug'
logger.transports.file.maxSize = 1002430 // 10M
logger.transports.file.format = '[{y}-{m}-{d} {h}:{i}:{s}.{ms}] [{level}]{scope} {text}'
logger.transports.console.format = '[{y}-{m}-{d} {h}:{i}:{s}.{ms}] [{level}]{scope} {text}'

logger.transports.file.resolvePath = () => {
    let date = new Date()
    date = date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate()
    let fileName = `${date}.log`
    return path.join("logs", fileName)
};

module.exports = logger
