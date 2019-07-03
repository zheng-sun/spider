import pymysql
import pymysql.cursors

class SpiderMysql(object):

    mysql_conn = None
    cursor = None

    def __init__(self):
        self.mysql_conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            db='suning_spider',
            user='root',
            passwd='root',
            charset='utf8',
            use_unicode=True
        )

        # 通过cursor 执行sql
        self.cursor = self.mysql_conn.cursor()