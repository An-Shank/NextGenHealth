from scrapy.spiders import Spider
from scrapy.item import Item , Field
from scrapy.selector import Selector
from scrapy.crawler import CrawlerProcess
from scrapy import Request
import re
from string import ascii_uppercase
import os
import csv

class MedUrl(Item) :
    Url = Field()

class MedSpider(Spider) :
    name = 'crawl'
    allowed_domain = ["medsplan.com"]
    urls = []
    base_url = "http://www.medsplan.com"
    for i in ascii_uppercase :
            urls.append("http://www.medsplan.com/AlphabeticalSearchFor/" + str(i))
    start_urls = urls
    allurls = []
    with open('medicinelist.csv' , 'r') as csvfile :
        fieldnames = ['Url']
        reader = csv.DictReader(csvfile , fieldnames = fieldnames)
        for row in reader :
            allurls.append(row['Url'])
    allurls.pop(0)

    def parse(self , response) :
        item = MedUrl()
        present = False
        select = Selector(response)
        bxpath = "//*[@class='listStyle3']/li/a"
        paths = select.xpath(bxpath + "/@href").extract()
        for path in paths :
            item['Url'] = MedSpider.base_url + path
            yield item

def main() :
    if os.path.isfile('sync.csv') :
        os.remove('sync.csv')
    process = CrawlerProcess({'USER_AGENT': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0' , 'FEED_FORMAT': 'csv' , 'FEED_URI': 'sync.csv'})
    process.crawl(MedSpider)
    process.start()
    u1 = []
    if os.path.isfile('database.csv') :
        csvfile = open('database.csv' , 'r')
        reader = csv.DictReader(csvfile)
        for row in reader :
            u1.append(row['MedUrl'])
        u1.pop(0)
        u2 = []
        csvfile.close()
        csvfile = open('sync.csv' , 'r')
        reader = csv.reader(csvfile)
        for row in reader :
            u2.append(''.join(r for r in row))
        csvfile.close()
        u2.pop(0)
        u3 = [i2 for i2 in u2 if i2 not in u1]
    else :
        u3 = u2
    csvfile = open('sync.csv' , 'w')
    writer = csv.DictWriter(csvfile , fieldnames = ['Url'])
    writer.writeheader()
    for i3 in u3 :
        writer.writerow({'Url' : i3})
    csvfile.close()

if __name__ == '__main__' : main()
