# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from .items import ESFItem,FangtianxiaSpiderItem


class FangtianxiaSpiderPipeline(object):



    def __init__(self):
        self.newhous = open('newhouse.json','a')
        self.esfhousw = open('erfhous.json','a')


    def process_item(self, item, spider):

        if isinstance(item,ESFItem):
            content = json.dumps(dict(item),ensure_ascii=False) +",\n"
            self.esfhousw.write(content.encode('utf-8'))
            return item

        if isinstance(item,FangtianxiaSpiderItem):
            content = json.dumps(dict(item),ensure_ascii=False) + ",\n"
            self.newhous.write(content.encode("utf-8"))
            return item

    def close_item(self,item):
        if isinstance(item,ESFItem):
            with open('newfang.json',"a") as f:
                f.write(item)
        else:
            with open('erfang.json',"a") as p:
                p.write(item)