# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem
import os

class DetectiveConanPipeline(FilesPipeline):
	def file_path(self, request, response=None, info=None):
		media_ext = os.path.splitext(request.url)[1]
		return 'full/{}{}'.format(request.meta.get('ep_id'), media_ext)
		
	def get_media_requests(self, item, info):
		for file_url in item['file_urls']:
			yield scrapy.Request(url=file_url, meta={'ep_id': item['ep_id']})