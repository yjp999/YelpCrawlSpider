# -*- coding: utf-8 -*-

# Scrapy settings for food project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'food'

SPIDER_MODULES = ['food.spiders']
NEWSPIDER_MODULE = 'food.spiders'

# LOG_LEVEL = 'ERROR'
# LOG_ENABLED = False

CONCURRENT_REQUESTS = 10


DOWNLOAD_DELAY = 1.5



ITEM_PIPELINES = {
   'food.pipelines.FoodPipeline': 300,
}

DOWNLOADER_MIDDLEWARES = {
	'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
	'food.middlewares.RotateUserAgentMiddleware': 100,
	'food.middlewares.ProxyMiddleware': 200,
}

AUTOTHROTTLE_ENABLED = True

PROXIES = [
	# {'ip_port': '45.79.217.88:3128', 'user_pass': 'yjp:abcd1234'},
	{'ip_port': '45.79.217.88:3128', 'user_pass': ''},
	# {'ip_port': '111.8.60.9:8123', 'user_pass': ''},
	# {'ip_port': '101.71.27.120:80', 'user_pass': ''},
	# {'ip_port': '122.96.59.104:80', 'user_pass': ''},
]