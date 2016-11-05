# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem


class SpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class DogRosterPicturePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")

        new_image_paths = []
        for image_path in image_paths:
            image_base = item['image_base']
            new_image_base = image_base + '/' + item['dog_name']

            new_image_path = image_path.replace('full/', '%s/' % item['dog_name'])
            if not os.path.exists(new_image_base):
                os.makedirs(new_image_base)

            try:
                os.rename(image_base + '/' + image_path, image_base + '/' + new_image_path)
            except Exception, e:
                print 'rename error', image_base + '/' + image_path, image_base + '/' + new_image_path

            new_image_paths.append(new_image_path)

        item['image_paths'] = new_image_paths
        return item

