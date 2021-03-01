"""
主程序入口
收集用例，生成测试报告
"""

import pytest
from config.path import reports_file_path
pytest.main(["--html={}".format(reports_file_path)])
