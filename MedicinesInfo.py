from scrapy.item import Item , Field
from scrapy.selector import Selector
from scrapy.spiders import Spider
from scrapy.crawler import CrawlerProcess

class MedicineItems(Item) :
    med_id = Field()
    details = Field()
    effects = Field()

class MedSpider(Spider) :
    name = 'ms'
    allowed_domain = ["medindia.net"]
    start_urls = ["http://www.medindia.net/doctors/drug_information/"]
    def parse(self , response) :
        select = Selector(response)
        item = ScrapyItem()
        products = select.xpath("/html/body/div[7]/div[3]/div/div[9]/div[2]/article[1]/h4/a/text()").extract()
