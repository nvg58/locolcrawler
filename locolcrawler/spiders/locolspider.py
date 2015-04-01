# -*- coding: utf-8 -*- 

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http.request import Request

from locolcrawler.items import LocolcrawlerItem


class LocolSpider(CrawlSpider):
    name = "locol"
    allowed_domains = ["sukienhay.com"]
    start_urls = [
        "http://sukienhay.com/cityevents.html?cityId=22"
    ]

    rules = (
        # Extract links for next pages
        Rule(SgmlLinkExtractor(allow=(),
                               restrict_xpaths='//ul[contains(@class, "pagination")][1]//a[contains(., "Tiếp theo")]'),
             callback='parse_listings', follow=True),
    )

    def parse_start_url(self, response):
        return self.parse_listings(response)

    def parse_listings(self, response):
        # hxs 	= HtmlXPathSelector(response)
        sel = Selector(response)
        events = sel.xpath('//*[@id="community-events-wrap"]/ul/li')
        for event in events:
            event_url = event.xpath('.//div[contains(@class, "event-title")]/a/@href')
            event_url = self.__normalise(event_url)
            event_url = self.__to_absolute_url(response.url, event_url)
            yield Request(event_url, callback=self.parse_details)

    def parse_details(self, response):
        sel = Selector(response)
        event = sel.xpath('//div[@class="event"]')
        # Populate event fields
        item = LocolcrawlerItem()
        item['title'] = event.xpath('.//div[contains(@class, "ctitleEvents")]/text()').extract()
        item['url'] = response.url
        item['thumbnail_url'] = event.xpath('.//*[contains(@class, "event-img")]//img/@src').extract()
        item['category'] = event.xpath('.//*[contains(@class, "event-category")]/text()').extract()
        item['date'] = event.xpath('.//div[contains(@class, "event-created")]/text()').extract()
        item['organizer'] = event.xpath('.//div[contains(@class, "event-organizer")]/text()').extract()
        item['location'] = event.xpath('.//div[contains(@class, "event-location")]/text()').extract()
        item['organizer'] = event.xpath('.//div[contains(@class, "eventcontactc")]/text()').extract()
        item['description'] = event.xpath('.//div[contains(@class, "event-desc")]/text()').extract()
        item['fee'] = event.xpath('.//div[contains(@class, "event-tickets")]/text()').extract()
        item = self.__normalise_item(item, response.url)
        return item

    def __normalise_item(self, item, base_url):
        # Loop item fields to sanitise data and standardise data types
        for key, value in vars(item).values()[0].iteritems():
            item[key] = self.__normalise(item[key])
        # Convert film URL from relative to absolute URL
        item['url'] = self.__to_absolute_url(base_url, item['url'])
        return item

    @staticmethod
    def __normalise(value):
        # Convert list to string
        value = value if type(value) is not list else ' '.join(value)
        # Trim leading and trailing special characters (Whitespaces, newlines, spaces, tabs, carriage returns)
        value = value.strip()
        return value

    @staticmethod
    def __to_absolute_url(base_url, link):
        import urlparse

        link = urlparse.urljoin(base_url, link)
        return link