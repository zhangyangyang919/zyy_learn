"""提现测试"""
import json
import pytest
import requests

from decimal import Decimal
from MiddleWare.helper import MiddleHandler

withdraw_excel_data = MiddleHandler.my_excel.read_data(sheet_name="withdraw")


@pytest.mark.parametrize("withdraw_data", withdraw_excel_data)
def test_withdraw(withdraw_data, loan_user_login, db_access):
    """提现测试用例"""
    request_method = withdraw_data["Request_method"]
    url = withdraw_data["Url"]
    headers = withdraw_data["Headers"]
    json_data = withdraw_data["Data"]
    expected_result = withdraw_data["Expect_result"]
    if "#member_id#" in json_data:
        member_id = loan_user_login["member_id"]
        json_data = json_data.replace("#member_id#", str(member_id))
    if "#token#" in headers:
        token = loan_user_login["token"]
        headers = headers.replace("#token#", token)
    if "#wrong_member_id#" in json_data:
        json_data = json_data.replace("#wrong_member_id#", str(loan_user_login["member_id"] + 10000))
    sql = "select leave_amount from member where id = {};".format(loan_user_login["member_id"])
    # 获取提现前db记录的余额
    money_withdraw_before = db_access.query_db(sql=sql)
    response = requests.request(method=request_method,
                                url=MiddleHandler.yaml_data["host"] + url,
                                headers=json.loads(headers),
                                json=json.loads(json_data))
    actual_result = response.json()["code"]
    # 获取提现前db记录的余额
    money_withdraw_after = db_access.query_db(sql=sql)
    try:
        assert actual_result == expected_result
        if actual_result == 0:
            withdraw_money = Decimal(str(json.loads(json_data)["amount"]))
            assert money_withdraw_after["leave_amount"] == money_withdraw_before["leave_amount"] - withdraw_money
    except AssertionError as e:
        MiddleHandler.my_logger.error("测试失败:{}".format(e))
        raise e
