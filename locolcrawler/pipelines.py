# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
import MySQLdb


class LocolcrawlerPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(user='root', '0u5a1n1x', 'locoldb', 'localhost', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        try:
            self.cursor.execute("""INSERT INTO events (title, url, thumbnail_url, category, time, date, location, organizer, description, max_participant)
                            VALUES (%s, %s)""",
                                (item['title'].encode('utf-8'),
                                 item['url'].encode('utf-8'),
                                 item['thumbnail_url'].encode('utf-8'),
                                 item['category'].encode('utf-8'),
                                 item['time'].encode('utf-8'),
                                 item['date'].encode('utf-8'),
                                 item['location'].encode('utf-8'),
                                 item['organizer'].encode('utf-8'),
                                 item['description'].encode('utf-8'),
                                 item['max_participants'].encode('utf-8')))

            self.conn.commit()
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])

        return item

