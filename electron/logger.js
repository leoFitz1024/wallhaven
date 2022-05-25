const logger = require('electron-log')
const path = require('path')

logger.transports.file.level = 'debug'
logger.transports.file.maxSize = 1002430 // 10M
logger.transports.file.format = '[{y}-{m}-{d} {h}:{i}:{s}.{ms}] [{level}]{scope} {text}'

logger.transports.file.resolvePath = () => {
    let date = new Date()
    date = date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate()
    let fileName = `${date}.log`
    return path.join("logs", fileName)
};

module.exports =  {
    info (param) {
        logger.info(param)
    },
    warn (param) {
        logger.warn(param)
    },
    error (param) {
        logger.error(param)
    },
    debug (param) {
        logger.debug(param)
    },
    verbose (param) {
        logger.verbose(param)
    },
    silly (param) {
        logger.silly(param)
    },
    setLevel(level){
        logger.transports.file.level = level
    },
    catchErrors(options) {
        logger.catchErrors(options)
    }
}
