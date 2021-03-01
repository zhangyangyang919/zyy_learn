"""封装获取数据库"""
# 导入pymysql
import pymysql
from pymysql.cursors import DictCursor


class DBHandler:
    def __init__(self,
                 host=None,
                 port=None,
                 user=None,
                 password=None,
                 charset="utf8",
                 database="futureloan",
                 cursorclass=DictCursor
                 ):
        """初始化"""
        # 建立链接
        self.connect = pymysql.connect(host=host,
                                       port=port,
                                       user=user,
                                       password=password,
                                       charset=charset,
                                       database=database,
                                       cursorclass=cursorclass
                                       )

    def query_db(self, sql, fetchone=True):
        """查询数据库"""
        # 获取游标
        cursor = self.connect.cursor()
        # 更新操作
        self.connect.commit()
        # sql语句查询 "select * from member limit 10;"
        cursor.execute(sql)
        # 关闭游标
        cursor.close()
        # 获取数据
        if fetchone:
            return cursor.fetchone()
        return cursor.fetchall()

    def close_db(self):
        """关闭数据库"""
        self.connect.close()
