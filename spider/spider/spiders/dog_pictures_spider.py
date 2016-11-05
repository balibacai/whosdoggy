# coding:utf-8
import scrapy
import json
import math
from spider.items import ImageItem


class DogPicturesSpider(scrapy.Spider):
    name = "dog_pictures"

    custom_settings = {
        'ITEM_PIPELINES': {
            'spider.pipelines.DogRosterPicturePipeline': 1,
        },
        'IMAGES_STORE': '/Users/Mist/Documents/dogs',
    }

    def start_requests(self):
        roster_file = file('rosters.json')
        dog_rosters = json.load(roster_file)

        url_pattern = 'http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ie=utf-8&oe=utf-8&word=%s&pn=%d'
        dog_pic_num = 10000
        # dog_pic_num = 1
        # dog_rosters = [dog_rosters.pop()]

        for roster in dog_rosters:
            dog_names = set(roster['alias'] + [roster['name']])
            each_pic_num = int(max(math.ceil(dog_pic_num / len(dog_names)), 1))

            for dog_name in dog_names:
                for page_num in range(0, each_pic_num, 30):
                    url = url_pattern % (dog_name, page_num)
                    yield scrapy.Request(url=url, meta={'dog_name': roster['name']}, callback=self.parse)

    def parse(self, response):
        jsonresponse = json.loads(response.body_as_unicode())
        data = jsonresponse['data']
        data.pop()

        thumb_urls = []
        for picture_block in data:
            thumb_url = picture_block['thumbURL']
            thumb_urls.append(thumb_url)

        item = ImageItem()
        item['dog_name'] = response.meta['dog_name']
        item['image_base'] = self.custom_settings['IMAGES_STORE']
        item['image_urls'] = thumb_urls
        yield item

