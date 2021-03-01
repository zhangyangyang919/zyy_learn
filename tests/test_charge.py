"""充值接口用例"""
import requests
import pytest
import json

from decimal import Decimal
from MiddleWare.helper import MiddleHandler

excel_charge_data = MiddleHandler.my_excel.read_data("charge")


@pytest.mark.parametrize("charge_data", excel_charge_data)
def test_charge(charge_data, loan_user_login, db_access):
    """测试充值接口"""
    request_method = charge_data["Request_method"]
    url = charge_data["Url"]
    headers = charge_data["Headers"]
    json_data = charge_data["Data"]
    expected_result = charge_data["Expect_result"]
    if "#loan_member_id#" in json_data:
        json_data = json_data.replace("#loan_member_id#", str(loan_user_login["member_id"]))
    if "#loan_token#" in headers:
        headers = headers.replace("#loan_token#", loan_user_login["token"])
    if "*wrong_member_id*" in json_data:
        json_data = json_data.replace("*wrong_member_id*", str(loan_user_login["member_id"] + 1))
    sql = "select leave_amount from member where id = {};".format(loan_user_login["member_id"])
    # 获取充值前db记录的余额
    money_charge_before = db_access.query_db(sql=sql)
    response = requests.request(method=request_method,
                                url=MiddleHandler.yaml_data["host"] + url,
                                headers=json.loads(headers),
                                json=json.loads(json_data))
    # 获取充值后db记录的余额
    money_charge_after = db_access.query_db(sql=sql)
    actual_result = response.json()["code"]
    try:
        assert actual_result == expected_result
        if actual_result == 0:
            charge_money = Decimal(str(json.loads(json_data)["amount"]))
            assert money_charge_after["leave_amount"] == money_charge_before["leave_amount"] + charge_money
    except AssertionError as e:
        MiddleHandler.my_logger.error("测试失败:{}{}".format(headers, json_data))
        raise e
