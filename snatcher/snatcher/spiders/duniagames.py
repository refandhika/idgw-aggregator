import scrapy
import json
from snatcher.items import SnatcherItem

class DuniagamesSpider(scrapy.Spider):
    name = "duniagames"
    allowed_domains = ["duniagames.co.id"]
    start_urls = ["https://api.duniagames.co.id/api/content-article/v1/article?slug=games&limit=10&page=1&status=published"]

    def parse(self, response):
        home_url = "https://duniagames.co.id"
        api_url = "https://api.duniagames.co.id"

        jsonResponse = json.loads(response.text)
        data = jsonResponse["data"]

        for i in data:
            #print("Item number ", idx)
            item = SnatcherItem()
            item['source'] = self.name
            item['site'] = home_url
            item['author'] = 'No Author'
            if (i['authorName']):
                item['author'] = i['authorName']
                print("Author = ", item['author'])
                item['link'] = home_url + "/discover/article/" + i['slug']
                print("URL = ", item['link'])
                item['image'] = i['image']
                print("Image =", item['image'])
                item['title'] = i['title']
                print("Title =", item['title'])

                apiContent = api_url + "/api/content-article/v1/article/body/" + i['slug'] + "?page=1&status=published"
                request = scrapy.Request(apiContent, self.parse_content)
                request.meta['item'] = item
                yield request
            print("\n==========================================================\n")

    def parse_content(self, response):
        item = response.meta['item']

        jsonResponse = json.loads(response.text)
        data = jsonResponse["data"]
        item['content'] = data['content']
        print("Content =", item['content'])

        yield item
