# -*- coding: utf-8 -*-
#from scrapy.settings.default_settings import DOWNLOAD_DELAY
#from scrapy.settings.default_settings import ITEM_PIPELINES

# Scrapy settings for fbo_scraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'moore_scraper'

SPIDER_MODULES = ['moore_scraper.spiders']
ITEM_PIPELINES = {'moore_scraper.pipelines.FboScraperExcelPipeline':0}
NEWSPIDER_MODULE = 'moore_scraper.spiders'

ROBOTSTXT_OBEY = True
RANDOMIZE_DOWNLOAD_DELAY = True
DOWNLOAD_DELAY = 3.0

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# !!! ATTENTION: PLEASE REPLACE WITH YOUR OWN WEBSITE IF YOU ARE GOING TO USE USER_AGENT!
USER_AGENT = 'moore_scraper (+http://research.umd.edu/)'
