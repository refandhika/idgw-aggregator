import scrapy
import re
from snatcher.items import SnatcherItem

class GamebrottSpider(scrapy.Spider):
    name = "gamebrott"
    allowed_domains = ["gamebrott.com"]
    start_urls = ["https://gamebrott.com/berita"]

    def parse(self, response):
        home_url = "https://gamebrott.com"
        for idx,i in enumerate(response.xpath("//article")):
            print("Item number ", idx)
            item = SnatcherItem()
            item['source'] = self.name
            item['site'] = home_url
            item['author'] = 'No Author'
            if (i.xpath("div[@class='jeg_thumb']/a/@href")):
                item['link'] = i.xpath("div[@class='jeg_thumb']/a/@href").get()
                print("URL = ", item['link'])

                request = scrapy.Request(item['link'], self.parse_content)
                request.meta['item'] = item
                yield request
            print("\n==========================================================\n")

    def parse_content(self, response):
        item = response.meta['item']

        item['author'] = response.xpath("//div[@class='jeg_meta_author']/a/text()").get()
        print("Author = ", item['author'])
        item['image'] = response.xpath("//div[@class='thumbnail-container']/img/@src").get()
        print("Image = ", item['image'])
        item['title'] = response.xpath("//h1[@class='jeg_post_title']/text()").get()
        print("Title = ", item['title'])
        item['content'] = response.xpath("//div[@class='content-inner  jeg_link_underline']").get()
        print("Content = ", item['content'])

        yield item
