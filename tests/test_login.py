"""登陆接口测试"""

import pytest
import requests
import json
from MiddleWare.helper import MiddleHandler

excel_login_data = MiddleHandler.my_excel.read_data("login")


@pytest.mark.parametrize("login_data", excel_login_data)
def test_login(login_data):
    """测试登陆模块"""
    login_data = json.dumps(login_data)
    login_data = MiddleHandler.replace_data(login_data)
    login_data = json.loads(login_data)
    request_method = login_data["Request_method"]
    url = login_data["Url"]
    headers = login_data["Headers"]
    json_data = login_data["Data"]
    expected_result = login_data["Expect_result"]
    if "*new*" in json_data:
        json_data = json_data.replace("*new*", MiddleHandler.get_random_phone_num())
    response = requests.request(method=request_method,
                                url=MiddleHandler.yaml_data["host"] + url,
                                headers=json.loads(headers),
                                json=json.loads(json_data))
    actual_result = response.json()["msg"]
    try:
        assert actual_result == expected_result
    except AssertionError as e:
        MiddleHandler.my_logger.error("测试失败:{}".format(e))
        raise e
    # finally:
    #     excel_login.write_data(sheet_name="login",
    #                            row=login_data["Case_ID"] + 1,
    #                            column=11,
    #                            data=str(response.json()))
