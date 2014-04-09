# encoding: utf-8
import time

from urllib2 import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from test.items import TestItem
from selenium import selenium


class MininovaSpider(CrawlSpider):
    name = 'testjs'
    #selenium
    #测试js的获取
    start_urls = ["http://alexa.chinaz.com/?domain=www.oschina.net"]
    allowed_domains = ["chinaz.com"]
    rules = [Rule(SgmlLinkExtractor(allow=('Domain=oschina.net')), callback='parse_torrent')]

    def parse_torrent(self, response):
        x = HtmlXPathSelector(response)
        torrent = TestItem()

        torrent['url'] = response.url
        torrent['name'] = ""
        torrent['price'] = ""
        torrent['memprice'] = ""
        torrent['press'] = ""
        torrent['publication'] = ""
        torrent['author'] = ""
        torrent['desc'] = ""
        torrent['belong'] = ""

        strlist = x.select("//h1/@title").extract()
        if len(strlist) > 0:
            torrent['name'] = strlist[0]


        print response.url
        print "========================================="


        url = ""

        url = response.url

        if url.count("Index.asp") > 0:
            aaa = selenium("localhost", 4444, "*chrome", response.url)
            aaa.start()

            aaa.open(response.url)

            time.sleep(2.5)

            IPNum = aaa.get_text("//td/span[@id='IpNum']/text()")
            print "****************************"
            print IPNum

            aaa.stop()

        return torrent