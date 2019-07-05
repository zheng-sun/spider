from .suning.category import CategorySpider as SuningCategorySpider
from .suning.product_list import GoodListSpider as SuningProductListSpider

def SpiderRun(url):
    SuningCategorySpider(url=url)
