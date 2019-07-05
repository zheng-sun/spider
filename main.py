from spider_lib.redis_connect import SpiderRedis
from spider_lib.mysql import SpiderMysql
import json
from spiders.suning.category import CategorySpider
from spiders.run import SpiderRun
spider_redis = SpiderRedis()

def add_next_task():
    jsonData = {}
    jsonData['project'] = 'suning'
    jsonData['spider'] = 'category'
    jsonData['url'] = 'http://list.suning.com'
    SpiderRedis().redis_conn.lpush('requests_wait_queue', json.dumps(jsonData))

# 启动应用
def execute():
    #add_next_task()
    for task in spider_redis.next_task():
        project = task['project']
        spider = task['spider']
        url = task['url']
        print('project:%s , spider: %s , url: %s ' % (project, spider, url))
        SpiderRun(url=url)

if __name__ == '__main__':
    execute()
