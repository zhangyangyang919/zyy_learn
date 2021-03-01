"""封装获取yaml文件数据"""


import yaml


def get_yaml_data(file_name):
    """读取yaml数据"""
    with open(file_name, encoding="utf-8") as f:
        yaml_data = yaml.load(f, Loader=yaml.SafeLoader)
        return yaml_data
