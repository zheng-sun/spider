import redis
import time
from lxml import etree
from spider_lib.requests import Request
from pipelines.suning.category import CategoryPipelines

class CategorySpider(object):
    name = 'suning.category'
    queue_key = 'Category_queue_list'

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
                print(Item)
                yield Item

    # 截取出分类id
    def jiequ(self, href):
        print(href)
        hrefitem = href[0].split('-', 2)
        return hrefitem[1]

    # 处理请求返回值
    def HandlerResponse(self, response):
        print('HandlerResposne')
        for item in self.parse(response):
            pass
            #self.insertCategory(item)

    # 开启爬虫
    def start(self, url):
        print('Category Spider start_request')
        #for url in self.next_request():
        Request().send_request(url=url, callback=self.HandlerResponse)

    def __del__(self):
        self.close()

    def close(self):
        print('爬虫抓取完成')