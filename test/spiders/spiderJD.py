# encoding: utf-8
import time

from urllib2 import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from test.items import TestItem
from selenium import selenium


class MininovaSpider(CrawlSpider):
    name = 'testjd'

    start_urls = ["http://list.jd.com/670-671-672-0-0-0-0-0-0-0-1-1-1-1-1-72-4137-0.html"]
    allowed_domains = ["jd.com"]
    rules = [Rule(SgmlLinkExtractor(allow=('item.jd.com/')), callback='myparse'), Rule(SgmlLinkExtractor(allow=('670-671-672-0-0-0-0-0-0-0-1-[^/]+4137-0.html', )), follow=True)]


    def myparse(self, response):
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


        aaa = selenium("localhost", 4444, "*chrome", response.url)
        aaa.start()
        aaa.open(response.url)
        time.sleep(2.5)

        desc = aaa.get_text("//div/div[@id='product-intro']/div[@id='name']/h1/text()")
        aaa.stop()

        print "****************************"
        print desc

        str = desc
        try:
            str = desc.decode("utf-8").encode("utf-8")
        except:
            try:
                str = desc.decode("gbk").encode("utf-8")
            except:
                pass

        torrent["desc"] = str

        return torrent