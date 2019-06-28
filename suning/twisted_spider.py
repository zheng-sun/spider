from twisted.web.client import getPage,defer
from twisted.internet import reactor
from twisted.python.failure import Failure
import uuid
import redis
import time

redis_conn = redis.Redis(host='127.0.0.1', port='6379')

def tasks_done(arg):
    reactor.stop()

def parse_page(res):
    print('12312321', res)
    print('解析结果 {}'.format(len(res)))

#初始化一个列表来存放getPage返回的defer对象
defer_list = []

urls = [
    'http://www.gov.cn',
    'https://www.douyu.com',
]

@defer.inlineCallbacks
def next_request():
    print('正在检测下一个爬取地址')
    block = 0
    while block < 2:
        print('检测下一个地址')
        url = redis_conn.lpop('twistedSpider:urls')
        if url is not None:
            print('检测到地址:%s' % url)
            print(type(url))
            print(url.decode('utf-8'))
            yield url
            block += 1
        time.sleep(2)

@defer.inlineCallbacks
def tasks():
    for url in urls:
        print('url')
        print(url)
        obj = getPage(url, )
        obj.addCallback(parse_page)
        defer_list.append(obj)
        yield defer_list

tasks()
#defer.DeferredList(defer_list).addBoth(tasks_done)
reactor.run()
