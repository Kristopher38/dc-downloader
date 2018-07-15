# -*- coding: utf-8 -*-
import scrapy
from detective_conan.items import DCVideo

class DownloadepsSpider(scrapy.Spider):
	name = 'downloadeps'
	#allowed_domains = ['https://otakustream.tv']
	custom_settings = {
		'ITEM_PIPELINES': {'scrapy.pipelines.files.FilesPipeline': 1},
		'FILES_STORE': 'C:\dc',
		'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
		'DOWNLOAD_TIMEOUT': 1800,
		'DOWNLOAD_WARNSIZE': 536870912
	}
	urls = []
	
	def __init__(self, first=None, last=None, *args, **kwargs):
		super(DownloadepsSpider, self).__init__(*args, **kwargs)
		if first and last:
			for i in range(int(first), int(last)+1):
				self.urls.append("https://otakustream.tv/anime/detective-conan/episode-"+str(i))
	
	def start_requests(self):
		for url in self.urls:
			yield scrapy.Request(url=url, callback=self.parse_ep_page, meta={'id': url[-3:]})
	
	def parse_ep_page(self, response):
		rel_url = response.xpath("//div[@id='Rapidvideo']/div[contains(@class, 'embed-responsive')]/iframe/@src")[0].extract()
		yield scrapy.Request(url=response.urljoin(rel_url), callback=self.parse_redirect, meta=response.meta)
		
	def parse_redirect(self, response):
		url = response.xpath("//iframe/@src")[0].extract()
		yield scrapy.Request(url=url, callback=self.parse_rawplayer, meta=response.meta)
		
	def parse_rawplayer(self, response):
		url = response.xpath("//video/source/@src").extract()
		#yield {'url': url, 'ep_id': response.meta['id']}
		yield DCVideo(file_urls=url, ep_id=response.meta['id'])
