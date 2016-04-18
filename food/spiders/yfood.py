# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.selector import Selector
from ..items import FoodItem
import codecs
import re,time
from scrapy.exceptions import CloseSpider
import pdb


class YfoodSpider(scrapy.Spider):
    name = "y1"
    allowed_domains = ["yelp.com"]
    # start_urls = (
    #     'http://www.yelp.com/',
    # )

    def __init__(self):
        self.cat = ["active"]
        self.searchmore_exp = ["Active Life"]
        self.domain = "http://www.yelp.com/c/"
        links, names = self.getcities()
        self.citylinks = links
        self.citynames = names

    def start_requests(self):
        for i, city in enumerate(self.citylinks):
            for j, cat in enumerate(self.cat):
                url = self.domain + city + '/'+cat
                cityname = self.citynames[i]
                exp = self.searchmore_exp[j]
                appends = dict()
                appends['city'] = cityname
                appends['cat'] = exp
                yield Request(url=url, callback=self.parse, meta={'appends': appends}, dont_filter=True)
            # pdb.set_trace()
            # time.sleep(1*10)

    def parse(self, response):
        if response.status ==503:
            raise CloseSpider("denied by remote server")
        sel = Selector(response)
        appends = response.meta['appends']
        cityname = appends['city']
        smexp = appends['cat']
        xpath_exp = '//a[text()="Search for more '+smexp+'"]/@href'
        if cityname=='香港':
            moreLink = ['http://www.yelp.com/search?cflt='+self.cat+'&find_loc=Hong+Kong', 'http://www.yelp.com/search?cflt='+self.cat+'&find_loc=香港島%2C+Hong+Kong']
        elif cityname=='Adelaide':
            moreLink = ['http://www.yelp.com/search?cflt='+self.cat+'&find_loc=Adelaide%2C+Adelaide+South+Australia%2C+Australia', 'http://www.yelp.com/search?cflt='+self.cat+'&find_loc=Adelaide+South+Australia+5000']
        elif cityname=='Park La Brea':
            moreLink = ['http://www.yelp.com/search?cflt='+self.cat+'&find_loc=South+La+Brea+Avenue%2C+Los+Angeles%2C+CA+90056', 'http://www.yelp.com/search?cflt='+self.cat+'&find_loc=Mid-Wilshire%2C+Los+Angeles%2C+CA', 'http://www.yelp.com/search?cflt='+self.cat+'&find_loc=North+La+Brea+Avenue%2C+Los+Angeles%2C+CA']
        else:
            searchmore = sel.xpath(xpath_exp).extract()[0]
            moreLink = [response.urljoin(searchmore)]

        for link in moreLink:
            yield Request(url=link, callback=self.parseBegin, meta={'appends': appends}, dont_filter=True)

    def parseBegin(self, response):
        if response.status ==503:
            raise CloseSpider("denied by remote server")
        sel = Selector(response)
        appends = response.meta['appends']
        cityName = appends['city']
        category = appends['cat']

        locations = self.getLocations(response.body)

        if locations == []:
            # self.logger.error("location is []: %s\t%s", response.url, str(cityName))
            return
        

        div_a = sel.xpath('//li[@class="regular-search-result"]/div/div[@class="biz-listing-large"]')
        for ii, div in enumerate(div_a):
            # pdb.set_trace()
            main = div.xpath('./div[1]/div/div[2]/h3/span/a[@class="biz-name"]')
            item = FoodItem()
            url = main.xpath('./@href').extract()
            item['url'] = response.urljoin(url[0])
            item['name'] = main.xpath('./span/text()').extract()[0]
            # pdb.set_trace()
            second = div.xpath('./div[2]')
            address = second.xpath('./address').extract()
            region = second.xpath('./span[@class="neighborhood-str-list"]/text()').extract()
            if address:
                item['address'] = self.filtertags(address[0])
            else:
                item['address'] = ""
            if region:
                item['region'] = (region[0]).strip()
            else:
                item['region'] = ""
            item['city'] = cityName.strip()
            item['category'] = category
            item['location'] = eval(locations[ii])
            yield item
        
        time.sleep(1.0)
        nextPage = sel.xpath('//a[@class="u-decoration-none next pagination-links_anchor"]/@href').extract()
        if nextPage:
            nextLink = response.urljoin(nextPage[0])
            yield Request(url=nextLink, callback=self.parseBegin, meta={'appends':appends}, dont_filter=True)



    def getcities(self):
        fr = codecs.open('citylist.txt', 'rb', encoding='utf-8')
        links = []
        names = []
        while True:
            line = fr.readline()
            if not line:
                fr.close()
                break
            link, name = line.split('\t')
            links.append(link)
            names.append(name)
        return (links, names)

    def filtertags(self, info):
        s = info
        s, num = re.subn('<address>', '', s)
        s, num = re.subn('</address>', '', s)
        s, num = re.subn('<br>', '', s)
        return s.strip()

    def getLocations(self, html):
        re_loc = re.compile(r'({"latitude":[^}]*?})')
        loc = re_loc.findall(html)
        if loc:
            return loc[1:]
        else:
            return []