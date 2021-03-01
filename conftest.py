"""共享夹具"""
import pytest
import requests

from MiddleWare.helper import MiddleHandler
from jsonpath import jsonpath


def login_support(phone_num, pwd):
    """夹具辅助"""
    request_method = "POST"
    url = MiddleHandler.yaml_data["host"] + "/member/login"
    headers = {"X-Lemonban-Media-Type": "lemonban.v2"}
    json = {"mobile_phone": phone_num,
            "pwd": pwd}
    response = requests.request(method=request_method,
                                url=url,
                                headers=headers,
                                json=json)
    member_id = jsonpath(response.json(), "$..id")[0]
    token = "Bearer" + " " + jsonpath(response.json(), "$..token")[0]
    leave_amount = jsonpath(response.json(), "$..leave_amount")[0]
    return {"member_id": member_id,
            "token": token,
            "leave_amount": leave_amount}


@pytest.fixture()
def loan_user_login():
    """普通用户登陆"""
    login_data = login_support(phone_num=MiddleHandler.yaml_data["loan_user"]["user_name"],
                               pwd=MiddleHandler.yaml_data["loan_user"]["password"])
    return login_data


@pytest.fixture()
def invest_user_login():
    """普通用户登陆"""
    login_data = login_support(phone_num=MiddleHandler.yaml_data["invest_user"]["user_name"],
                               pwd=MiddleHandler.yaml_data["invest_user"]["password"])
    return login_data


@pytest.fixture()
def admin_user_login():
    """管理员用户登陆"""
    login_data = login_support(phone_num=MiddleHandler.yaml_data["admin_user"]["user_name"],
                               pwd=MiddleHandler.yaml_data["admin_user"]["password"])
    return login_data


@pytest.fixture()
def loan_add(loan_user_login):
    """新增项目"""
    token = loan_user_login["token"]
    member_id = loan_user_login["member_id"]
    request_method = "POST"
    url = MiddleHandler.yaml_data["host"] + "/loan/add"
    headers = {"X-Lemonban-Media-Type": "lemonban.v2",
               "Authorization": token}
    json = {"member_id": member_id,
            "title": "报名Python全栈自动化课程",
            "amount": 10000.00,
            "loan_rate": 12.0,
            "loan_term": 12,
            "loan_date_type": 1,
            "bidding_days": 5}
    response = requests.request(method=request_method,
                                url=url,
                                headers=headers,
                                json=json)
    loan_id = jsonpath(response.json(), "$..id")[0]
    amount = jsonpath(response.json(), "$..amount")[0]
    return {"loan_id": loan_id,
            "amount": amount}


@pytest.fixture()
def db_access():
    """处理数据的链接"""
    my_db = MiddleHandler.db_class()
    yield my_db
    my_db.close_db()
