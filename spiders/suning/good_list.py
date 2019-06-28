import redis
import requests
import time
import lxml

redis_conn = redis.Redis()

class GoodListSpider(object):
    name = 'suning.good_list'
    queue_key = 'good_list_queue_list'

    # 开启爬虫
    def start(self):
        print('GoodListSpider Spider start_request')
        for url in self.next_request():
            self.send_request(url=url, callback=self.parse)

    #返回下一个爬取地址
    def next_request(self):
        while True:
            url = redis_conn.lpop(self.queue_key)
            print('下个爬取地址检索中: %s' % url)
            if url is not None:
                print(url)
                print(url)
                yield url
            time.sleep(1)

    # 发送请求
    def send_request(self, url, callback):
        print('send_request')
        print(url)
        print(callback)
        response = requests.get(url=url)
        callback(response)

    # 处理返回值
    def parse(self, response):
        print('parse response')
        print(response)

    def add_next_task(self):
        pass

if __name__ == '__main__':
    GoodListSpider().start()