# -*- coding: utf-8 -*-
import scrapy
from new51cto.items import New51CtoItem

class NewsSpider(scrapy.Spider):
    name = 'news'
    # allowed_domains = ['www.51cto.com']
    urls = []

    for i in range(10):
        urls.append("http://blog.51cto.com/original/0/" + str(i))

    start_urls = urls

    def parse(self, response):
        items = []
        for each in response.xpath('//div[@class="r_li"]'):
            item = New51CtoItem()
            item["link"] = each.xpath('.//h4/a/@href').extract()[0]
            item["title"] = each.xpath('.//h4/a/text()').extract()[0]
            item["author"] = each.xpath('.//em/a/text()').extract()[0]
            items.append(item)

            # yield item

        for link in items:
            yield scrapy.Request(link["link"],meta={"link":link},callback=self.parse_content)

    def parse_content(self,response):
        # print response.text
        item = response.meta["link"]

        for article in response.xpath('//div[@class="showContent"]'):
            item["content"] = article.xpath('./p/text()').extract()
            yield item




        pass
