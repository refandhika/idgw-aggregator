import scrapy
import re
from snatcher.items import SnatcherItem

class KotakgameSpider(scrapy.Spider):
    name = "kotakgame"
    allowed_domains = ["kotakgame.com"]
    start_urls = [
        "https://www.kotakgame.com/berita/"
    ]

    def parse(self, response):
        home_url = "https://www.kotakgame.com"
        for idx,i in enumerate(response.xpath("//div[contains(concat(' ', normalize-space(@class), ' '), ' detailfeature ')]/div[@class='bawah']")):
            print("Item number ", idx)
            item = SnatcherItem()
            item['source'] = self.name
            item['site'] = home_url
            item['author'] = 'No Author'
            if (i.xpath("div/div[@class='author']//span[@class='txtcreate txt20']/text()")):
                author = i.xpath("div/div[@class='author']//span[@class='txtcreate txt20']/text()").get()
                if (author):
                    item['author'] = re.sub(r"\s\s+", " " , author)
                    item['author'] = re.sub(r" \|.*$", "", item['author'])
                    print("Author = ", item['author'])
                    item['link'] = home_url + i.xpath("div[@class='wrapimgnews']/a/@href").get()
                    print("URL = ", item['link'])
                    item['image'] = home_url + i.xpath("div[@class='wrapimgnews']/a/img/@src").get()
                    print("Image =", item['image'])

                    request = scrapy.Request(item['link'], self.parse_content)
                    request.meta['item'] = item
                    yield request
            print("\n==========================================================\n")

    def parse_content(self, response):
        item = response.meta['item']

        item['title'] = response.xpath("//h3[@class='judulh3']/span/text()").get()
        print("Title =", item['title'])
        item['content'] = response.xpath("//div[@class='isinewsp']").get()
        print("Content =", item['content'])

        yield item
