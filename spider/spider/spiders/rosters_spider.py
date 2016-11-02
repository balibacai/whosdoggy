# coding:utf-8
import scrapy
import re
from spider.items import RosterItem


class RostersSpider(scrapy.Spider):
    name = "rosters"

    def start_requests(self):
        urls = [
            'http://baike.baidu.com/view/1008598.htm',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        dog_blocks = response.css('table').pop().css('td > div.para > a')
        for block in dog_blocks:
            name = block.css('::text').extract_first()
            baike_url = response.urljoin(block.css('::attr(href)').extract_first())

            item = RosterItem()
            item['detail'] = baike_url
            item['name'] = name
            # yield item

            yield scrapy.Request(baike_url, callback=self.parse_baike_alias)

    def parse_baike_alias(self, response):
        categories = response.css('div.basic-info').css('dl > dt')
        name = response.css('h1::text').extract_first()
        item = RosterItem()
        item['detail'] = response.url
        item['name'] = name
        item['alias'] = []

        for category in categories:
            if len(category.css('::text').re(ur'别\s+称')) == 1:
                alias_desc = category.xpath('string(following-sibling::dd[1])').extract_first().strip('\n')
                alias_list = re.split(u'、|，|/|,', alias_desc)
                item['alias'] = alias_list

        yield item