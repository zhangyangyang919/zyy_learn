"""注册接口测试"""

import pytest
import requests
import json

from MiddleWare.helper import MiddleHandler

excel_data = MiddleHandler.my_excel.read_data(sheet_name="register_test")


@pytest.mark.parametrize('test_data', excel_data)
def test_register_case(test_data):
    """登陆用例测试"""
    test_data = json.dumps(test_data)
    MiddleHandler.get_random_phone_num()
    test_data = MiddleHandler.replace_data(test_data)
    test_data = json.loads(test_data)
    request_method = test_data['Request_method']
    url = MiddleHandler.yaml_data["host"] + test_data['Url']
    headers = test_data['Headers']
    json_data = test_data['Data']
    expect_result = test_data['Expect_result']
    response = requests.request(method=request_method, url=url, headers=eval(headers), json=json.loads(json_data))
    actual_result = response.json()['code']
    try:
        assert actual_result == expect_result
    except AssertionError as e:
        MiddleHandler.my_logger.error('测试用例失败:{}{}'.format(e, test_data))
        raise e
    # finally:
    #     my_excel.write_data(sheet_name="register_test",
    #                         row=test_data['Case_ID'] + 1,
    #                         column=11,
    #                         data=str(response.json()))
