"""中间层"""
import re

import faker

from common.db_handler import DBHandler
from common.excel_handler import ExcelHandler
from common.logger_handler import get_logger
from common.yaml_handler import get_yaml_data
from config.path import config_file_path, logs_file_path, data_file_path


class MiddleDb(DBHandler):
    """DB中间层处理"""
    def __init__(self):
        yam_data = get_yaml_data(file_name=config_file_path)
        super().__init__(host=yam_data["db"]["host"],
                         port=yam_data["db"]["port"],
                         user=yam_data["db"]["user"],
                         password=yam_data["db"]["password"])


class MiddleHandler:
    """中间层处理"""

    # yaml模块
    yaml_data = get_yaml_data(file_name=config_file_path)

    # 需要替换的数据
    admin_user_name = yaml_data["admin_user"]["user_name"]
    admin_user_pwd = yaml_data["admin_user"]["password"]
    loan_user_name = yaml_data["loan_user"]["user_name"]
    loan_user_pwd = yaml_data["loan_user"]["password"]
    invest_user_name = yaml_data["invest_user"]["user_name"]
    invest_user_pwd = yaml_data["invest_user"]["password"]
    phone_number = ""

    @classmethod
    def replace_data(cls, string, pattern="#(.*?)#"):
        """替换数据"""
        replace_data = re.finditer(pattern=pattern, string=string)
        for data in replace_data:
            old_data = data.group()
            new_data = str(getattr(cls, data.group(1)))
            string = string.replace(old_data, new_data)
        return string

    # logger模块
    my_logger = get_logger(logger_name=yaml_data["logger"]["logger_name"],
                           logger_level=yaml_data["logger"]["logger_level"],
                           stream_handler_level=yaml_data["logger"]["stream_handler_level"],
                           file_handler_level=yaml_data["logger"]["file_handler_level"],
                           file_name=logs_file_path,
                           format_data=yaml_data["logger"]["format_data"])

    # excel模块
    my_excel = ExcelHandler(file_path=data_file_path)

    # db模块
    db_class = MiddleDb

    # support模块
    @classmethod
    def get_random_phone_num(cls):
        """获取任意手机号"""
        fake = faker.Faker(locale="zh_CN")
        while True:
            phone_num = fake.phone_number()
            my_db = MiddleHandler.db_class()
            phone_num_db = my_db.query_db(sql="select * from member where mobile_phone = {};".format(phone_num))
            my_db.close_db()
            if not phone_num_db:
                cls.phone_number = phone_num
                return phone_num


# if __name__ == "__main__":
#     a = MiddleHandler()
#     print(a.get_random_phone_num())
#     string = "#phone_number#"
#     print(a.replace_data(string))



