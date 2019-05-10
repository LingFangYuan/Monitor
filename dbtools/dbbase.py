import pandas as pd
import cx_Oracle
import pymysql
from dbtools.get_sqltext import get_sql
import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    import pymssql  # 需忽略警告的模块


class DbBase(object):

    def __init__(self, host, port, user, passwd, db):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db
        self.conn = None
        self.cursor = None
        self.get_conn()

    def __del__(self):
        self.close_conn()

    def get_conn(self):
        """
        获取 conn连接和cursor游标
        :return: conn,cursor
        """
        pass

    def close_conn(self):
        """
        关闭 conn连接和cursor游标
        :return:
        """
        self.cursor.close()
        self.conn.close()

    def query_sql(self, sql):
        """
        执行sql脚本
        :param cursor: 访问游标
        :param sql: 执行的sql脚本
        :return:
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def query(self, path):
        """
        连接、执行、关闭
        :param path: 需要执行的sql脚本路径
        :return:
        """
        sql = get_sql(path)
        return self.query_sql(sql), self.cursor.description

    def get_DataFrame(self, path, idx=None):
        """"
        连接、执行、关闭
        :param path: 需要执行的sql脚本路径
        :return: pandas 数据帧
        """
        sql = get_sql(path)
        return pd.read_sql(sql, self.conn, index_col=idx)


class Oracle(DbBase):

    def __init__(self, user, passwd, db):
        super().__init__(host=None, port=None, user=user, passwd=passwd, db=db)

    def get_conn(self):
        """
        获取 conn连接和cursor游标
        :return: conn,cursor
        """
        self.conn = cx_Oracle.connect(self.user + '/' + self.passwd + '@' + self.db)  # 连接数据库
        self.cursor = self.conn.cursor()  # 获取cursor


class MySql(DbBase):

    def get_conn(self):
        """"
        获取
        conn连接和cursor游标
        :return: conn, cursor
        """
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.passwd,
                                    db=self.db)  # 连接数据库
        self.cursor = self.conn.cursor()  # 获取cursor


class MsSql(DbBase):

    def __init__(self, host, port, user, passwd, db):
        super().__init__(':'.join([host, str(port)]), None, user, passwd, db)

    def get_conn(self):
        """"
        获取
        conn连接和cursor游标
        :return: conn, cursor
        """
        self.conn = pymssql.connect(host=self.host, port=self.port, user=self.user, password=self.passwd,
                                    database=self.db)  # 连接数据库
        self.cursor = self.conn.cursor()  # 获取cursor


if __name__ == '__main__':
    oracle = Oracle()
    mysql = MySql()
    mssql = MsSql()
    df1 = oracle.get_DataFrame('../sql/test1.sql')
    df2 = mysql.get_DataFrame('../sql/test2.sql')
    df3 = mssql.get_DataFrame('../sql/test3.sql')
    print(df1)
    print(df2)
    print(df3)
