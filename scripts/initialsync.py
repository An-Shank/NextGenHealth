from scrapy.spiders import Spider
from scrapy.item import Item , Field
from scrapy.selector import Selector
from scrapy.crawler import CrawlerProcess
from scrapy import Request
import re
from string import ascii_uppercase
import os
import csv
import hashlib

class MedUrl(Item) :
    Url = Field()

# visit_urls = []
# class MedSpider(Spider):
#     name = 'crawl'
#     allowed_domain = ["medsplan.com"]
#     urls = []
#     base_url = "http://www.medsplan.com/"
#     for i in ascii_uppercase :
#             urls.append("http://www.medsplan.com/AlphabeticalSearchFor/" + str(i))
#     start_urls = urls
#     def parse(self , response) :
#         select = Selector(response)
#         item = MedItem()
#         medname = []
#         count = 1
#         bxpath = "//*[@class='listStyle3']/li/a"
#         paths = select.xpath(bxpath).extract()
#         # if response.url not in visit_urls :
#         for path in paths :
#             m = select.xpath(bxpath + "/text()").extract()
#             murl = select.xpath(bxpath + "/@href").extract()
#             # if m :
#             #         medname.append(m[0])
#             # else :
#             #         break
#             # visit_urls.append(response.url)
#             req = Request(MedSpider.base_url + str(murl[0]) , callback = self.parse_next , dont_filter = True)
#             # count += 1
#             req.meta['item'] = item
#             yield req
#
#     def parse_next(self , response) :
#         select = Selector(response)
#         item = MedItem()
#         brand_name = select.xpath("//*[@id='ContentPlaceHolder1_lblBrandName']/text()").extract()
#         gen_name = select.xpath("//*[@id='ContentPlaceHolder1_lblGenericName']/text()").extract()
#         detail = select.xpath("//*[@id='ContentPlaceHolder1_tbUses']/text()").extract()
#         seffect = select.xpath("//*[@id='ContentPlaceHolder1_tbSideEffects']/text()").extract()
#         ibname = set([b.lstrip().replace('\n' , ',').strip().encode(encoding = 'UTF-8') for b in brand_name])
#         item['BrandName'] = list(ibname)
#         iname = set([g.lstrip().replace('\n' , ',').strip().encode(encoding = 'UTF-8') for g in gen_name])
#         item['GenName'] = list(iname)
#         idesc = [','.join(d.lstrip().replace(' ' , '#').split()).replace('#' , ' ').encode(encoding = 'UTF-8') for d in detail]
#         item['Desc'] = list(idesc)
#         ieffect = [','.join(s.lstrip().replace(' ' , '#').split()).replace('#' , ' ').encode(encoding = 'UTF-8') for s in seffect]
#         item['Effects'] = list(ieffect)
#         return item

class MedSpider(Spider) :
    name = 'crawl'
    allowed_domain = ["medsplan.com"]
    urls = []
    base_url = "http://www.medsplan.com"
    for i in ascii_uppercase :
            urls.append("http://www.medsplan.com/AlphabeticalSearchFor/" + str(i))
    start_urls = urls
    def parse(self , response) :
        item = MedUrl()
        select = Selector(response)
        bxpath = "//*[@class='listStyle3']/li/a"
        paths = select.xpath(bxpath + "/@href").extract()
        for path in paths :
            item['Url'] = MedSpider.base_url + path
            yield item

def main() :
    if os.path.isfile('medicinelist.csv') :
        os.remove('medicinelist.csv')
    process = CrawlerProcess({'USER_AGENT': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0' , 'FEED_FORMAT': 'csv' , 'FEED_URI': 'medicinelist.csv'})
    process.crawl(MedSpider)
    process.start()

if __name__ == '__main__' : main()
