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
                               restrict_xpaths='//ul[contains(@class, "pagination")][1]//a[contains(., "theo")]'),
             callback='parse_listings', follow=True),
    )

    def parse_start_url(self, response):
        unicode(response.body.decode(response.encoding)).encode('utf-8')

        return self.parse_listings(response)

    def parse_listings(self, response):
        unicode(response.body.decode(response.encoding)).encode('utf-8')

        sel = Selector(response)
        events = sel.xpath('//*[@id="community-events-wrap"]/ul/li')
        for event in events:
            event_urls = event.xpath('.//div[contains(@class, "event-title")]/a/@href').extract()
            for event_url in event_urls:
                event_url = self.__normalise(event_url)
                event_url = self.__to_absolute_url(response.url, event_url)

                yield Request(event_url, callback=self.parse_details)

    def parse_details(self, response):
        unicode(response.body.decode(response.encoding)).encode('utf-8')

        sel = Selector(response)
        event = sel.xpath('//div[@class="event"]')
        # Populate event fields
        item = LocolcrawlerItem()
        item['title'] = event.xpath('.//div[contains(@class, "ctitleEvents")]/h1/text()').extract()
        item['url'] = response.url
        item['thumbnail_url'] = event.xpath('.//*[contains(@class, "event-img")]//img/@src').extract()
        item['category'] = event.xpath('.//*[contains(@class, "event-category")]/a[1]/text()').extract()
        item['time'] = event.xpath('.//div[contains(@class, "event-created")]/b/text()').extract()
        item['date'] = event.xpath('.//div[contains(@class, "event-created")]/b/a/text()').extract()
        # item['organizer'] = event.xpath('.//div[contains(@class, "event-organizer")]/text()').extract()
        item['location'] = event.xpath('.//div[contains(@class, "event-location")]/text()')[0].extract()
        item['organizer'] = event.xpath('.//div[contains(@class, "eventcontactc")]/textarea/text()').extract()
        item['description'] = event.xpath('.//div[@class = "event-desc"]').extract()
        item['max_participants'] = event.xpath('.//div[contains(@class, "event-tickets")]/text()').extract()
        item = self.__normalise_item(item, response.url)
        return item

    def __normalise_item(self, item, base_url):
        # Loop item fields to sanitise data and standardise data types
        for key, value in vars(item).values()[0].iteritems():
            item[key] = self.__normalise(item[key])

        # Convert film URL from relative to absolute URL
        item['url'] = self.__to_absolute_url(base_url, item['url'])
        return item

    def __normalise(self, value):
        # Convert list to string
        value = value if type(value) is not list else ' '.join(value)
        # Trim leading and trailing special characters (Whitespaces, newlines, spaces, tabs, carriage returns)
        value = value.strip()

        return value

    def __to_absolute_url(self, base_url, link):
        import urlparse

        link = urlparse.urljoin(base_url, link)

        return link