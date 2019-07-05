from spider_lib.mysql import SpiderMysql

class CategoryPipelines(object):

    def insertCategory(self, item):
        sql = """replace into category(category_id, category_name) values (%s, %s)"""
        SpiderMysql().cursor.execute(sql, (item['category_id'], item['category_name']))
        SpiderMysql().mysql_conn.commit()
