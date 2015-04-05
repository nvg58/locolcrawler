# -*- coding: utf-8 -*-

# Scrapy settings for locolcrawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
# http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'locolcrawler'

SPIDER_MODULES = ['locolcrawler.spiders']
NEWSPIDER_MODULE = 'locolcrawler.spiders'

# ITEM_PIPELINES = ['locolcrawler.pipelines.LocolcrawlerPipeline']

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'locolcrawler (+http://www.yourdomain.com)'
