from spider_lib.redis_connect import SpiderRedis
from spider_lib.mysql import SpiderMysql
import json
from spiders.suning.category import CategorySpider


# 检测是否存在下一个爬取任务
def next_task():
    value = SpiderRedis().redis_conn.lpop('requests_wait_queue')
    if value is not None:
        print(value)
        print(type(value))
        yield json.loads(value)

def add_next_task():
    jsonData = {}
    jsonData['project'] = 'suning'
    jsonData['spider'] = 'category'
    jsonData['url'] = 'http://list.suning.com'
    SpiderRedis().redis_conn.lpush('requests_wait_queue', json.dumps(jsonData))

# 启动应用
def execute():
    #add_next_task()
    for task in next_task():
    # #     project = task['project']
    # #     spider = task['spider']
    # #     url = task['url']
        CategorySpider().start(url=task['url'])

if __name__ == '__main__':
    execute()