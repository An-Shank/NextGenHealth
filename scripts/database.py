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

class MedItem(Item):
    MedUrl = Field()
    BrandName = Field()
    GenName = Field()
    Desc = Field()
    Effects = Field()

class InfoSpider(Spider) :
    name = 'info'
    allowed_domain = ["medsplan.com"]
    urls = []
    file = 'medicinelist.csv'
    if os.path.isfile('sync.csv') :
        file = 'sync.csv'
    with open(file , 'r') as csvfile :
        fieldnames = ['Url']
        reader = csv.DictReader(csvfile , fieldnames = fieldnames)
        for row in reader :
            urls.append(row['Url'])
    urls.pop(0)
    start_urls = urls

    def parse(self , response) :
        select = Selector(response)
        item = MedItem()
        item['MedUrl'] = response.url
        brand_name = select.xpath("//*[@id='ContentPlaceHolder1_lblBrandName']/text()").extract()
        gen_name = select.xpath("//*[@id='ContentPlaceHolder1_lblGenericName']/text()").extract()
        detail = select.xpath("//*[@id='ContentPlaceHolder1_tbUses']/text()").extract()
        seffect = select.xpath("//*[@id='ContentPlaceHolder1_tbSideEffects']/text()").extract()
        ibname = set([b.lstrip().replace('\n' , ',').strip().encode(encoding = 'UTF-8') for b in brand_name])
        item['BrandName'] = list(ibname)
        iname = set([g.lstrip().replace('\n' , ',').strip().encode(encoding = 'UTF-8') for g in gen_name])
        item['GenName'] = list(iname)
        idesc = [','.join(d.lstrip().replace(' ' , '#').split()).replace('#' , ' ').encode(encoding = 'UTF-8') for d in detail]
        item['Desc'] = list(idesc)
        ieffect = [','.join(s.lstrip().replace(' ' , '#').split()).replace('#' , ' ').encode(encoding = 'UTF-8') for s in seffect]
        item['Effects'] = list(ieffect)
        yield item

def main() :
    exist = False
    if os.path.isfile('database.csv') :
        exist = True
    process = CrawlerProcess({'USER_AGENT': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0' , 'FEED_FORMAT': 'csv' , 'FEED_URI': 'medicines.csv'})
    process.crawl(InfoSpider)
    process.start()
    new = []
    csvfile = open('medicines.csv' , 'r')
    reader = csv.reader(csvfile)
    for row in reader :
        new.append(row)
    fieldnames = new[0]
    new.pop(0)
    csvfile.close()
    csvfile = open('database.csv' , 'a')
    writer = csv.DictWriter(csvfile , fieldnames = fieldnames)
    if exist == False :
        writer.writeheader()
    for n in new :
        writer.writerow({fieldnames[0] : n[0] , fieldnames[1] : n[1] , fieldnames[2] : n[2] , fieldnames[3] : n[3] , fieldnames[4] : n[4]})
    csvfile.close()
    os.remove('medicines.csv')

if __name__ == '__main__' : main()
