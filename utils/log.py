import logging
import logging.handlers
import os
from utils.decorators import singleton


@singleton
class SingletonLogging:
    """
    单例日志类
    """

    def __init__(self, logger_name, logfile_dir):
        """
        初始化日志属性
        :param logger_name: 日志器名称
        :param logfile_dir: 日志文件夹名称
        """
        self.logger_name = logger_name

        # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        BASE_DIR = BASE_DIR.replace("\\", "/")
        self.logfile_path = BASE_DIR + logfile_dir

        os.makedirs(self.logfile_path, exist_ok=True)

    def get_logger(self):
        """
        配置日志
        :return: 日志器
        """
        # 获取日志器
        logger = logging.getLogger(self.logger_name)
        # 设置日志等级
        logger.setLevel(logging.DEBUG)

        # 处理所有日志
        # 获取处理器
        all_handler = logging.handlers.TimedRotatingFileHandler(filename=self.logfile_path + "/all.log",
                                                                encoding="utf-8", when='midnight')
        # 获取格式器
        all_formatter = logging.Formatter('%(asctime)s [%(filename)s:%(lineno)d] %(levelname)s - %(message)s')
        # 添加格式器
        all_handler.setFormatter(all_formatter)
        # 添加处理器
        logger.addHandler(all_handler)

        # Commenting out the stdout streaming for production server.
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(fmt=all_formatter)
        logger.addHandler(stream_handler)

        # # 处理error日志
        # # 获取处理器
        # error_handler = logging.handlers.TimedRotatingFileHandler(filename=self.logfile_path + "/error.log",
        #                                                           encoding="utf-8", when='midnight')
        # # 设置格式器
        # error_formatter = logging.Formatter("%(levelname)s - %(asctime)s - %(filename)s[:%(lineno)d] - %(message)s")
        # # 添加格式器
        # error_handler.setFormatter(error_formatter)
        # # 设置处理器处理的日志等级
        # error_handler.setLevel(logging.ERROR)
        # # 添加处理器
        # logger.addHandler(error_handler)

        return logger


logger = SingletonLogging(logger_name="monitor", logfile_dir="/logs").get_logger()

if __name__ == '__main__':
    logger.error("Test error log")

