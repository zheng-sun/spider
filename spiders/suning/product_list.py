import redis
import requests
import time
from lxml import etree
import pymysql
import pymysql.cursors

redis_conn = redis.Redis()

class RFPDupeFilter(object):
    # 对发送请求进行加密
    # def add_request_hishory(self, key, request):
    #     redis_conn.lindex(key, request)

    def check_request_PFPDuper(self, key, request):
        print(redis_conn.lindex(key, request))

class GoodListSpider(object):
    name = 'suning.good_list'
    queue_key = 'productListQueue'

    # 开启爬虫
    def start(self):
        print('GoodListSpider Spider start_request')
        for url in self.next_request():
            self.send_request(url=url, callback=self.parse)

    #返回下一个爬取地址
    def next_request(self):
        while True:
            url = redis_conn.rpop(self.queue_key)
            print('下个爬取地址检索中: %s , 时间: %s' % (url, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
            if url is not None:
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

    # 添加下一个请求地址
    def add_next_request(self, url, queueKey = queue_key ):
        print(url)
        redis_conn.lpush(queueKey, url)

    # 处理返回值
    def parse(self, response):
        print('parse response')
        print(response)
        html = etree.HTML(response.text)
        isNextPage = True
        next_page_list = html.xpath('//div[@class="search-page page-fruits clearfix"]/a/@href')
        print(next_page_list)
        for next_page in next_page_list:
            if next_page.find('html') > 0:
                next_page = 'http://list.suning.com'+next_page
                #self.add_next_request(next_page, 'productListQueue')

        # 获取商品链接
        product_link = html.xpath('//a[@class="sellPoint"]/@href')
        print(product_link)
        for product_page in product_link:
            print('ProductQueue')
            self.add_next_request('http:'+product_page, 'productQueue')

    def add_next_task(self):
        pass

if __name__ == '__main__':
    GoodListSpider().start()