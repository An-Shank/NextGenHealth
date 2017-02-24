from scrapy.spiders import Spider
from scrapy.item import Item , Field
from scrapy.selector import Selector
from scrapy.crawler import CrawlerProcess
from scrapy import Request
import re
from string import ascii_uppercase

class MedItem(Item):
        Name = Field()
        Desc = Field()
        Effects = Field()

visit_urls = []
class MedSpider(Spider):
        name = 'crawl'
        allowed_domain = ["medsplan.com"]
        urls = []
        base_url = "http://www.medsplan.com/"
        for i in ascii_uppercase :
                urls.append("http://www.medsplan.com/AlphabeticalSearchFor/" + str(i))
        start_urls = urls
        def parse(self , response) :
                select = Selector(response)
                item = MedItem()
                medname = []
                count = 1
                if response.url not in visit_urls :
                    while count < 5 :
                            m = select.xpath("//*[@id='scrollbar1']/div[2]/div/ul/li[" + str(count) + "]/a/text()").extract()
                            murl = select.xpath("//*[@id='scrollbar1']/div[2]/div/ul/li[" + str(count) + "]/a/@href").extract()
                            if m :
                                    medname.append(m[0])
                            else :
                                    break
                            visit_urls.append(response.url)
                            req = Request(MedSpider.base_url + str(murl[0]) , self.parse_next)
                            count += 1
                            item = req
                            yield item

        def parse_next(self , response) :
                select = Selector(response)
                item = MedItem()
                gen_name = select.xpath("//*[@id='ContentPlaceHolder1_lblGenericName']/text()").extract()
                detail = select.xpath("//*[@id='ContentPlaceHolder1_tbUses']/text()").extract()
                seffect = select.xpath("//*[@id='ContentPlaceHolder1_tbSideEffects']/text()").extract()
                iname = set([g.replace("\n" , " ").strip() for g in gen_name])
                item['Name'] = list(iname)
                idesc = [d.replace("\n" , " ").strip() for d in detail]
                item['Desc'] = list(idesc)
                ieffect = [s.replace("\n" , " ").strip() for s in seffect]
                item['Effects'] = list(ieffect)
                return item

def main() :
        process = CrawlerProcess({'USER_AGENT': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0' , 'FEED_FORMAT': 'csv' , 'FEED_URI': 'MedicineList.csv'})
        process.crawl(MedSpider)
        process.start()

if __name__ == '__main__' : main()
