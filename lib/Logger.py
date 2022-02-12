


class Logger:
    LOGGER = None

    @staticmethod


    @staticmethod
    def debug(log):
        Logger.LOGGER.debug(log)

    @staticmethod
    def info(log):
        Logger.LOGGER.info(log)

    @staticmethod
    def warning(log):
        Logger.LOGGER.warning(log)

    @staticmethod
    def error(log):
        Logger.LOGGER.error(log)

    @staticmethod
    def critical(log):
        Logger.LOGGER.critical(log)


if __name__ == '__main__':
    Logger.init("E:\PycharmProjects\wallhaven")
    Logger.error("xxx")
