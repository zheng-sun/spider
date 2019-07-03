import redis
import requests
import time
from lxml import etree
import pymysql
import pymysql.cursors
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

redis_conn = redis.Redis()

class RFPDupeFilter(object):
    # 对发送请求进行加密
    # def add_request_hishory(self, key, request):
    #     redis_conn.lindex(key, request)

    def check_request_PFPDuper(self, key, request):
        print(redis_conn.lindex(key, request))

class ProductSpider(object):
    name = 'sunning.product'
    queue_key = 'productQueue'

    def __init__(self):
        #chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument('--headless')
        #chrome_options.add_argument('--disable-gpu')
        #D:\\PythonCode\\scrapy\\chromedriver_74.exe
        #self.browser = webdriver.Chrome(executable_path='E:\\PythonCode\\scrapy\\chromedriver_73.exe', chrome_options=chrome_options)
        self.browser = webdriver.Chrome("D:\\PythonCode\\scrapy\\chromedriver_74.exe")
        self.browser.set_page_load_timeout(120)

    # 开启爬虫
    def start(self):
        print('ProductSpider Spider start_request')
        #for url in self.next_request():
        #http://product.suning.com/0000000000/10565963785.html
        #http://product.suning.com/0000000000/10605010791.html
        #https://product.suning.com/0000000000/10606656295.html
        url = 'http://product.suning.com/0000000000/10606656295.html'
        self.send_request(url=url, callback=self.parse)

    #返回下一个爬取地址
    def next_request(self):
        #while True:
        url = redis_conn.rpop(self.queue_key)
        print('下个爬取地址检索中: %s , 时间: %s' % (url, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        if url is not None:
            print(url)
            yield url
            #time.sleep(1)

    # 发送请求
    def send_request(self, url, callback):
        print('send_request')
        print(url)
        #response = requests.get(url=url)
        try:
            self.browser.get(url)
            #self.browser.execute_script()
            self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        except TimeoutException as e:
            print('超时')
            self.browser.execute_script('window.stop()')
        time.sleep(2)
        print(self.browser.current_url)
        #print(self.browser.page_source)
        callback(self.browser.page_source)
        #return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source,encoding="utf-8", request=request)

    # 添加下一个请求地址
    def add_next_request(self, url, queueKey = queue_key ):
        print(url)
        redis_conn.lpush(queueKey, url)

    # 处理返回值
    def parse(self, response):
        print('parse response')
        #print(response)
        html = etree.HTML(response)
        # 获取商品名称
        ProductName = html.xpath('//h1[@id="itemDisplayName"]/text()')
        print(ProductName)
        if len(ProductName) > 1:
            print(ProductName[1])
        else:
            print(ProductName[0])

        #获取商品参考价格
        # ProductSmallPrice = html.xpath('//del[@class="small-price"]/text()')
        # print(ProductSmallPrice)
        # #获取商品价格
        # ProductPrice = html.xpath('//span[@class="mainprice"]/text()')
        # print(ProductPrice)
        # 获取商品的属性
        product_attr = html.xpath('//div[@class="tzm"]/dl')
        for product in product_attr:
            if len(product.xpath('@style')) == 0:
                print(product.xpath('dt/span/text()'))   #属性名称
                print(product.xpath('dd/ul/li/@title'))  #属性值名称
                print(product.xpath('dd/ul/li/@cid'))    #属性值ID
                #print(product.xpath('//li/@sku'))        #子商品id

        # 筛选出子商品sku
        # SubProductSku = html.xpath('//div[@class="tzm"]/dl/dd/ul/li/@sku')
        # print(SubProductSku)

    def add_next_task(self):
        pass

if __name__ == '__main__':
    ProductSpider().start()