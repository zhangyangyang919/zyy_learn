"""封装日志收集器"""
# 函数封装
import logging


def get_logger(logger_name=None,
               logger_level=None,
               stream_handler_level=None,
               file_handler_level=None,
               file_name=None,
               format_data=None):
    """获取日志处理器"""
    # 初始化日志收集器
    logger_handler = logging.getLogger(logger_name)
    logger_handler.setLevel(logger_level)
    # 设置日志输出格式
    fmt = logging.Formatter(format_data)
    # 初始化日志处理器
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(stream_handler_level)
    stream_handler.setFormatter(fmt)
    logger_handler.addHandler(stream_handler)
    # 初始化文件日志处理器
    if file_name:
        file_handler = logging.FileHandler(file_name, encoding='utf-8')
        file_handler.setLevel(file_handler_level)
        file_handler.setFormatter(fmt)
        logger_handler.addHandler(file_handler)
    return logger_handler


# 类封装
# class Logger_handler(logging.Logger):
#     def __init__(self,
#                  stream_handler_level="DEBUG",
#                  file_handler_level="INFO",
#                  file_name=None,
#                  format_data="time:%(asctime)s--%(levelname)s:%(name)s:%(message)s--%(filename)s---%(lineno)s"
#                  ):
#         super().__init__(name='root', level='DEBUG')
#         # 设置日志输出格式
#         fmt = logging.Formatter(format_data)
#         # 初始化日志处理器
#         stream_handler = logging.StreamHandler()
#         stream_handler.setLevel(stream_handler_level)
#         stream_handler.setFormatter(fmt)
#         self.addHandler(stream_handler)
#         # 初始化文件日志处理器
#         if file_name:
#             file_handler = logging.FileHandler(file_name, encoding='utf-8')
#             file_handler.setLevel(file_handler_level)
#             file_handler.setFormatter(fmt)
#             self.addHandler(file_handler)
#
#
# my_logger = Logger_handler(file_name='test.log')
# my_logger.info('运行正常')
# my_logger.error('报错')