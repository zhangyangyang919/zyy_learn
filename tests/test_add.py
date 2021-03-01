"""新增项目"""
import json

import pytest
import requests
from MiddleWare.helper import MiddleHandler


excel_add_data = MiddleHandler.my_excel.read_data(sheet_name="add")


@pytest.mark.parametrize("add_data", excel_add_data)
def test_add_project(add_data, loan_user_login):
    """新增项目测试用例"""
    method = add_data["Request_method"]
    url = add_data["Url"]
    headers_data = add_data["Headers"]
    json_data = add_data["Data"]
    expect_result = add_data["Expect_result"]
    if "#member_id#" in json_data:
        member_id = loan_user_login["member_id"]
        json_data = json_data.replace("#member_id#", str(member_id))
    if "#token#" in headers_data:
        token = loan_user_login["token"]
        headers_data = headers_data.replace("#token#", token)
    if "#wrong_member_id#" in json_data:
        member_id = loan_user_login["member_id"]
        json_data = json_data.replace("#wrong_member_id#", str(member_id + 10000))
    response = requests.request(method=method,
                                url=MiddleHandler.yaml_data["host"] + url,
                                headers=json.loads(headers_data),
                                json=json.loads(json_data))
    resp_data = response.json()
    try:
        assert resp_data["code"] == expect_result
    except AssertionError as e:
        MiddleHandler.my_logger.error("测试用例失败{}".format(e))
        raise e
