"""审核项目"""
import pytest
import requests
import json

from jsonpath import jsonpath

from MiddleWare.helper import MiddleHandler

audit_excel_data = MiddleHandler.my_excel.read_data("audit")


@pytest.mark.parametrize("audit_data", audit_excel_data)
def test_audit(audit_data, loan_add):
    """审核项目测试用例"""
    audit_data = json.dumps(audit_data)
    audit_data = MiddleHandler.replace_data(audit_data)
    audit_data = json.loads(audit_data)
    method = audit_data["Request_method"]
    url = audit_data["Url"]
    headers_data = audit_data["Headers"]
    json_data = audit_data["Data"]
    expect_result = audit_data["Expect_result"]
    if "*loan_id*" in json_data:
        load_id = loan_add["loan_id"]
        json_data = json_data.replace("*loan_id*", str(load_id + 10000))
    response = requests.request(method=method,
                                url=MiddleHandler.yaml_data["host"] + url,
                                headers=json.loads(headers_data),
                                json=json.loads(json_data))
    resp = response.json()
    if audit_data["support_data"]:
        support_data = json.loads(audit_data["support_data"])
        for prop_name, path_name in support_data.items():
            set_value = jsonpath(resp, path_name)[0]
            setattr(MiddleHandler, prop_name, set_value)
    expect_result = json.loads(expect_result)
    for key, value in expect_result.items():
        try:
            assert jsonpath(resp, key)[0] == value
        except AssertionError as e:
            MiddleHandler.my_logger.error("测试未通过{}{}".format(e, response.text))
            raise e
