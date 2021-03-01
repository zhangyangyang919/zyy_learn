import json

import pytest
import requests
from jsonpath import jsonpath

from MiddleWare.helper import MiddleHandler

excel_invest_data = MiddleHandler.my_excel.read_data(sheet_name="invest")


@pytest.mark.parametrize("invest_data", excel_invest_data)
def test_invest(invest_data, loan_add, invest_user_login):
    invest_data = json.dumps(invest_data)
    invest_data = MiddleHandler.replace_data(invest_data)
    invest_data = json.loads(invest_data)
    url = invest_data["Url"]
    request_method = invest_data["Request_method"]
    json_data = invest_data["Data"]
    headers = invest_data["Headers"]
    expect_result = invest_data["Expect_result"]
    if "*above_amount*" in json_data:
        above_amount = loan_add["amount"]
        json_data = json_data.replace("*above_amount*", str(above_amount + 100))
    if "*wrong_member_id*" in json_data:
        member_id = invest_user_login["member_id"]
        json_data = json_data.replace("*wrong_member_id*", str(member_id + 100))
    if "*wrong_loan_id*" in json_data:
        loan_id = loan_add["loan_id"]
        json_data = json_data.replace("*wrong_loan_id*", str(loan_id + 100))
    resp = requests.request(method=request_method,
                            url=MiddleHandler.yaml_data["host"] + url,
                            json=json.loads(json_data),
                            headers=json.loads(headers))
    if invest_data["support_data"]:
        support_data = json.loads(invest_data["support_data"])
        for prop_key, value in support_data.items():
            value_data = jsonpath(resp.json(), value)[0]
            setattr(MiddleHandler, prop_key, value_data)
    print(invest_data)
    try:
        assert resp.json()["code"] == expect_result
    except AssertionError as e:
        MiddleHandler.my_logger.error("测试用例失败{}{}".format(json_data, resp.text))
        raise e


