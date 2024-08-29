# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sys
import MySQLdb
import hashlib

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.http import Request

class MySQLStorePipeline(object):
	def __init__(self):
		self.conn = MySQLdb.connect(user='1dGWUs3r!', passwd='1dGWp4Ss!', db='idgwoffsite', host='localhost', charset="utf8mb4", use_unicode=True)
		self.cursor = self.conn.cursor()

	def process_item(self, item, spider):
		try:
			self.cursor.execute("""INSERT INTO articles (title, content, author, link, source, image, site) VALUES (%s, %s, %s, %s, %s, %s, %s)""",
				(item['title'].encode('utf-8'),
					item['content'].encode('utf-8'),
					item['author'].encode('utf-8'),
					item['link'].encode('utf-8'),
					item['source'].encode('utf-8'),
					item['image'].encode('utf-8'),
                    item['site'].encode('utf-8')))
			self.conn.commit()

		except MySQLdb.Error as e:
			print("Error %d: %s" % (e.args[0], e.args[1]))

		return item

class DuplicatesPipeline(object):

    def __init__(self):
        self.links_seen = set()

    def process_item(self, item, spider):
        if item['link'] in self.links_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.links_seen.add(item['link'])
            return item
