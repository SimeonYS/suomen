import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import SuomenItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class SuomenSpider(scrapy.Spider):
	name = 'suomen'
	start_urls = ['https://www.suomenpankki.fi/fi/media-ja-julkaisut/uutiset/?y=']

	def parse(self, response):
		post_links = response.xpath('//h3/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//div[@class="lead-text"][1]/text()[last()]').get()
		date = re.findall(r'\d+\.\d+\.\d+',date)
		title = response.xpath('//h1/text()').get()
		content = response.xpath('//article[@class="columns small-12 release"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=SuomenItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
