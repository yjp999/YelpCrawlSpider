#-*- coding:utf-8 -*-

import random
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware
import base64
from settings import PROXIES

class RotateUserAgentMiddleware(UserAgentMiddleware):
	def __init__(self, user_agent=''):
		self.user_agent = user_agent
 
	def process_request(self, request, spider):
		#这句话用于随机选择user-agent
		ua = random.choice(self.user_agent_list)
		if ua:
			request.headers.setdefault('User-Agent', ua)

	user_agent_list = [
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
		"Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
		"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
		"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
		"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
		"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
		"Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
		"Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0",
		"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20130401 Firefox/31.0",
		"Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16",
		"Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
		"Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02",
		"Opera/9.80 (Windows NT 6.1; U; es-ES) Presto/2.9.181 Version/12.00",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
		"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
		"Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
		
	]

class ProxyMiddleware(object):
	def process_request(self, request, spider):
		proxy = random.choice(PROXIES)
		if proxy['user_pass'] is not None:
			request.meta['proxy'] = "http://%s" % proxy['ip_port']
			encoded_user_pass = base64.encodestring(proxy['user_pass'])
			request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
		else:
			request.meta['proxy'] = "http://%s" % proxy['ip_port']
