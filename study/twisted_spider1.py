from twisted.web.client import getPage,defer
from twisted.internet import reactor
from twisted.python.failure import Failure
import uuid
import redis
import time

redis_conn = redis.Redis(host='127.0.0.1', port='6379')

class SpiderRequest(object):
    
    @defer.inlineCallbacks
    def sendRequest(request_url):
        obj = getPage(request_url,)
        obj.addCallback(self.parse_page)

    def parse_page(self, res):
        print('12312321', res)
        print('解析结果 {}'.format(len(res)))


class CrawlerProcess(object):

    def stop(self):
        return defer.DeferredList([c.stop() for c in list(self.crawlers)])

    def start(self):
        print('CrawlerProcess start')
        tp = reactor.getThreadPool()
        tp.adjustPoolsize(maxthreads=2)
        reactor.addSystemEventTrigger('before', 'shutdown', self.stop)
        reactor.run(installSignalHandlers=False)


def execute():
    CrawlerProcess().start()

if __name__ == '__main__':
    execute()

