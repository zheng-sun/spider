import redis
import traceback

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
