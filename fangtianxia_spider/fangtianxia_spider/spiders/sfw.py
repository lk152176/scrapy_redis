# -*- coding: utf-8 -*-
import scrapy
import re
from fangtianxia_spider.items import FangtianxiaSpiderItem,ESFItem
from scrapy_redis.spiders import RedisSpider

class SfwSpider(RedisSpider):
    name = 'sfw'
    allowed_domains = ['fang.com']

    # start_urls = ['https://www.fang.com/SoufunFamily.html']
    redis_key = "fang:start_urls"

    def parse(self, response):
        trs = response.xpath("//div[@class='outCont']//tr")
        province = None

        for tr in trs:
            tds = tr.xpath(".//td[not(@class)]")
            province_td = tds[0]
            province_text = province_td.xpath(".//text()").get()
            province_text = re.sub(r"\s", "", province_text)
            if province_text:
                province=province_text
            if province=='其它':
                #如果爬取的是海外城市则不进行爬取
                continue
            city_td = tds[1]
            city_links = city_td.xpath(".//a")

            for city_link in  city_links:
                city = city_link.xpath(".//text()").get()
                city_url = city_link.xpath(".//@href").get()
                module = city_url.split('.')
                one = module[0]
                mid = module[1]
                last = module[2]

                newhouse_url = one + '.newhouse.'+ mid + '.' + last +'house/s/'
                esf_url = one + '.esf.'+ mid + '.'+last

                if 'bj' in one:
                    newhouse_url = "https://newhouse.fang.com/house/s/"
                    esf_url = "https://esf.fang.com/"
                yield scrapy.Request(url=newhouse_url, callback=self.parse_newhouse,meta={'info': (province, city)})
                yield scrapy.Request(url=esf_url, callback=self.parse_esf, meta={'info': (province, city)},dont_filter=True)


    def parse_newhouse(self,response):
        print(response.url)
        province,city = response.meta.get('info')
        lis = response.xpath("//div[@class='nl_con clearfix']//li")
        for li in lis:
            if not li.xpath('.//div[@class="nlc_details"]'):
                continue
            name=li.xpath('.//div[@class="nlcd_name"]/a/text()').get().strip()
            house_text=li.xpath('.//div[@class="house_type clearfix"]/a/text()').getall()
            house_text=list(map(lambda x:re.sub(r'\s','',x),house_text))
            rooms=list(filter(lambda x:x.endswith('居'),house_text))
            area = "".join(li.xpath('.//div[@class="house_type clearfix"]/text()').getall())
            area=re.sub(r'\s|－|/','',area)
            district=li.xpath(".//div[@class='address']/a/@title").get()
            sale=li.xpath("//div[@class='fangyuan pr']/span/text()").get()
            price=''.join(li.xpath(".//div[@class='nhouse_price']//text()").getall())
            price=re.sub(r'\s|广告','',price)
            origin_url="https:"+li.xpath(".//div[@class='nlcd_name']/a/@href").get()
            item=FangtianxiaSpiderItem(province=province,city=city,name=name,price=price,rooms=rooms,area=area,address=district,sale=sale,origin_url=origin_url)
            yield item
        next_url=response.xpath("//a[@class='next']/@href").get()
        #自动翻页
        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url),callback=self.parse_newhouse,meta={'info':(province,city)})






    def parse_esf(self, response):
        #  print(response.url)
        province, city = response.meta.get('info')
        item = ESFItem(province=province, city=city)
        print(response.xpath('//*[@id="kesfqbfylb_A01_01_03"]/dd[1]/h4/a/span/text()').get())
        dls = response.xpath("//dl[@dataflag='bg']")
        for dl in dls:
            name = dl.xpath(".//dd/h4/a/span/text()").get()
            item['name'] = name
            infos = dl.xpath("./dd/p/text()").getall()
            infos = list(map(lambda x: re.sub(r'\s', '', x), infos))
            for info in infos:
                if '厅' in info:
                    item['rooms'] = info
                elif '层' in info:
                    item['floor'] = info
                elif '向' in info:
                    item['toward'] = info
                elif '年' in info:
                    item['year'] = info.replace('建', '')
                elif '㎡' in info:
                    item['area'] = info
            item['address'] = dl.xpath(".//p[@class='add_shop']/span/text()").get()
            price = "".join(dl.xpath(".//dd[@class='price_right']/span[1]//text()").getall())
            item['price'] = price
            item['unity'] = dl.xpath(".//dd[@class='price_right']/span[2]/text()").get()
            item['origin_url'] = response.url + dl.xpath(".//dd/h4/a/@href").get()
            print(item)
            yield item
        next_url = response.xpath('//*[@id="list_D10_15"]/p[1]/a/@href').get()
        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url), callback=self.parse_esf,meta={'info': (province, city)}, dont_filter=True)




