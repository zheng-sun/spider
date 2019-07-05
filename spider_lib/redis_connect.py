import redis
import traceback
import json

class SpiderRedis(object):

    redis_conn = None

    def __init__(self, host='127.0.0.1', port='6379', database='0'):
        # try:
        #     print(host)
        self.redis_conn = redis.Redis(host=host, port=port, db=database)
        #     print(self.redis_conn)
        # except Exception:
        #     print('发生异常', Exception)
        #     #traceback.print_exc('redis链接失败, 请检查redis配置和服务器！')

    def add_task(self, task):
        jsonData = json.dumps(task)
        if jsonData is not None:
            self.redis_conn.lpush('requests_wait_queue', jsonData)

    # 检测是否存在下一个爬取任务
    def next_task(self):
        value = self.redis_conn.lpop('requests_wait_queue')
        if value is not None:
            print(value)
            print(type(value))
            yield json.loads(value)
