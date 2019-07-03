import redis
import requests
import time
from lxml import etree
import spider.spider_lib.redis_connect as redis_connect

class CategorySpider(object):
    name = 'suning.category'
    queue_key = 'Category_queue_list'

    # 开启爬虫
    def start(self, url):
        print('Category Spider start_request')
        #for url in self.next_request():
        self.send_request(url=url, callback=self.HandlerResponse)

    #返回下一个爬取地址
    def next_request(self):
        while True:
            url = redis_conn.lpop(self.queue_key)
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

    # 处理请求返回值
    def HandlerResponse(self, response):
        print('HandlerResposne')
        for item in self.parse(response):
            pass
            #self.insertCategory(item)

    def insertCategory(self, item):
        sql = """insert into category(category_id, category_name) values (%s, %s)"""
        cursor.execute(sql, (item['category_id'], item['category_name']))
        connect.commit()

    # 添加下一个请求地址
    def add_next_request(self, url, queueKey = queue_key ):
        print(url)
        redis_conn.lpush(queueKey, url)

    # 解析请求返回值
    def parse(self, response):
        print('parse response')
        print(response)
        html = etree.HTML(response.text)
        search_main = html.xpath('//div[@class="search-main introduce clearfix"]/div')
        for category in search_main:
            # 二级分类
            box_data = category.xpath('div[@class="title-box clearfix"]')
            for category_2 in box_data:
                Item = {}
                href = category_2.xpath('div[@class="t-left fl clearfix"]/a/@href')
                title = category_2.xpath('div[@class="t-left fl clearfix"]/a/text()')
                Item['category_id'] = self.jiequ(href)
                Item['category_name'] = title
                yield Item

                self.add_next_request('http:'+href[0], 'productListQueue')

    # 截取出分类id
    def jiequ(self, href):
        print(href)
        hrefitem = href[0].split('-', 2)
        return hrefitem[1]

    #添加下一个任务
    def add_next_task(self):
        pass

if __name__ == '__main__':
    CategorySpider().start()