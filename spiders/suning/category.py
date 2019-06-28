import redis
import requests
import time
from lxml import etree
import pymysql
import pymysql.cursors

redis_conn = redis.Redis()

# 连接数据库
connect = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    db='suning_spider',
    user='root',
    passwd='root',
    charset='utf8',
    use_unicode=True
)
# 通过cursor 执行sql
cursor = connect.cursor()

class CategorySpider(object):
    name = 'suning.category'
    queue_key = 'Category_queue_list'

    # 开启爬虫
    def start(self):
        print('Category Spider start_request')
        for url in self.next_request():
            self.send_request(url=url, callback=self.HandlerResponse)

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

    # 处理请求返回值
    def HandlerResponse(self, response):
        print('HandlerResposne')
        for item in self.parse(response):
            self.insertCategory(item)

    def insertCategory(self, item):
        sql = """insert into category(category_id, category_name) values (%s, %s)"""
        cursor.execute(sql, (item['category_id'], item['category_name']))
        connect.commit()

    # 解析请求返回值
    def parse(self, response):
        print('parse response')
        print(response)
        html = etree.HTML(response.text)
        print(html)
        search_main = html.xpath('//div[@class="search-main introduce clearfix"]/div')
        print(search_main)
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

    # 截取出分类id
    def jiequ(self, href):
        print(href)
        hrefitem = href[0].split('-', 2)
        return hrefitem[1]

    def add_next_task(self):
        pass

if __name__ == '__main__':
    CategorySpider().start()