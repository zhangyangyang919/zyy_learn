"""路径处理"""

import os

from datetime import datetime

# 获取当前时间戳
current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

# 获取文件目录
path_dir = os.path.dirname(os.path.abspath(__file__))
config_dir = os.path.dirname(path_dir)

# 获取日志路径
logs_path = os.path.join(config_dir, "logs")
if not os.path.exists(logs_path):
    os.mkdir(logs_path)
logs_file = current_time + ".log"
logs_file_path = os.path.join(logs_path, logs_file)


# 获取报告路径
reports_path = os.path.join(config_dir, "reports")
if not os.path.exists(reports_path):
    os.mkdir(reports_path)
report_file = current_time + ".html"
reports_file_path = os.path.join(reports_path, report_file)

# 获取测试数据路径
data_path = os.path.join(config_dir, "data")
if not os.path.exists(data_path):
    os.mkdir(data_path)
data_file = "p2p_test_cases.xlsx"
data_file_path = os.path.join(data_path, data_file)


# 获取配置文件路径
config_file = "config_file.yaml"
config_file_path = os.path.join(path_dir, config_file)
