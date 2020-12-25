# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class MovieCommentPipeline:
    def process_item(self, item, spider):
        if not item.get('star'):
            item['star'] = 0
        elif item['star'] == '力荐':
            item['star'] = 5
        elif item['star'] == '推荐':
            item['star'] = 4
        elif item['star'] == '还行':
            item['star'] = 3
        elif item['star'] == '较差':
            item['star'] = 2
        elif item['star'] == '很差':
            item['star'] = 1
        return item
