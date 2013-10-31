# encoding: utf-8

from urllib2 import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from test.items import TestItem

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item
#from douban.items import DoubanItem
import re
#
# class GroupSpider(CrawlSpider):
#     name = "Group"
#     allowed_domains = ["douban.com"]
#     start_urls = [
#         "http://www.douban.com/group/explore?tag=%E8%B4%AD%E7%89%A9",
#         "http://www.douban.com/group/explore?tag=%E7%94%9F%E6%B4%BB",
#         "http://www.douban.com/group/explore?tag=%E7%A4%BE%E4%BC%9A",
#         "http://www.douban.com/group/explore?tag=%E8%89%BA%E6%9C%AF",
#         "http://www.douban.com/group/explore?tag=%E5%AD%A6%E6%9C%AF",
#         "http://www.douban.com/group/explore?tag=%E6%83%85%E6%84%9F",
#         "http://www.douban.com/group/explore?tag=%E9%97%B2%E8%81%8A",
#         "http://www.douban.com/group/explore?tag=%E5%85%B4%E8%B6%A3"
#     ]
#
#     rules = [
#         Rule(SgmlLinkExtractor(allow=('/group/[^/]+/$', )), callback='parse_group_home_page', process_request='add_cookie'),
#         #Rule(SgmlLinkExtractor(allow=('/group/[^/]+/discussion\?start\=(\d{1,4})$', )), callback='parse_group_topic_list', process_request='add_cookie'),
#         Rule(SgmlLinkExtractor(allow=('/group/explore\?tag', )), follow=True, process_request='add_cookie'),
#         ]
#
#     def __get_id_from_group_url(self, url):
#         m = re.search("^http://www.douban.com/group/([^/]+)/$", url)
#         if(m):
#             return m.group(1)
#         else:
#             return 0
#
#
#
#     def add_cookie(self, request):
#         request.replace(cookies=[
#         ]);
#         return request;
#
#     def parse_group_topic_list(self, response):
#         self.log("Fetch group topic list page: %s" % response.url)
#         pass
#
#
#     def parse_group_home_page(self, response):
#
#         self.log("Fetch group home page: %s" % response.url)
#
#         hxs = HtmlXPathSelector(response)
#         item = DoubanItem()
#
#         #get group name
#         item['groupName'] = hxs.select('//h1/text()').re("^\s+(.*)\s+$")[0]
#
#         #get group id
#         item['groupURL'] = response.url
#         groupid = self.__get_id_from_group_url(response.url)
#
#         #get group members number
#         members_url = "http://www.douban.com/group/%s/members" % groupid
#         members_text = hxs.select('//a[contains(@href, "%s")]/text()' % members_url).re("\((\d+)\)")
#         item['totalNumber'] = members_text[0]
#
#         #get relative groups
#         item['RelativeGroups'] = []
#         groups = hxs.select('//div[contains(@class, "group-list-item")]')
#         for group in groups:
#             url = group.select('div[contains(@class, "title")]/a/@href').extract()[0]
#             item['RelativeGroups'].append(url)
#         #item['RelativeGroups'] = ','.join(relative_groups)
#         return item<span><span style="line-height:20px;"> </span></span>






class MininovaSpider(CrawlSpider):
    name = 'test'


    #start_urls = ["http://yuedu.baidu.com/book/list/21001?show=1"]
    start_urls = ["http://yuedu.baidu.com/book/list/0?od=0&show=1&pn=0"]
    #allowed_domains = ["douban.com"]
    rules = [Rule(SgmlLinkExtractor(allow=('/ebook/[^/]+fr=booklist')), callback='parse_torrent'), Rule(SgmlLinkExtractor(allow=('/book/list/[^/]+pn=[^/]+', )), follow=True)]

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

        print response.url+"    "+torrent['name']

        strlist = x.select("//div[@class='doc-info-price']//span[@class='txt-now-price-num']/text()").extract()
        if len(strlist) > 0:
            torrent['price'] = strlist[0]

        strlist = x.select("//div[@class='privilege-price']/span[contains(@style, 'color:')]/text()").extract()
        if len(strlist) > 0:
            torrent['memprice'] = strlist[0]

        strlist = x.select("//ul[@class='doc-info-org']/li/text()").extract()

        count = len(strlist)
        if count > 0:
            torrent['author'] = strlist[0]

        if count > 1:
            torrent['publication'] = strlist[1]

        if count > 2:
            torrent['press'] = strlist[2]


        strlist = x.select("//div[@class='des-content']/p/text()").extract()
        if len(strlist) > 0:
            torrent['desc'] = strlist[0]

        strlist = x.select("//li/a[contains(@data-logsend, 'send')]/text()").extract()

        belong = ""
        index = 0
        for str in strlist:
            index += 1
            if index <= 1:
                continue

            if len(belong) <= 0:
                belong += str
            else:
                belong += "->"+str

        torrent['belong'] = belong

        print belong


        # strlist = x.select("//div[@class='bd']/ul/li/text()").extract()
        # for item in strlist:
        #
        #     if item.count("出版社：".decode("utf-8")) > 0:
        #         print "======="+item+"   "
        #     else:
        #         print item

        # if len(title) > 0:
        #     try:
        #         torrent['name'] = title[0].decode("gbk").encode("utf-8")
        #         #torrent['name'] = title[0].decode("utf-8").encode("utf-8")
        #     except:
        #         try:
        #             torrent['name'] = title[0].decode("utf-8").encode("utf-8")
        #         except:
        #             torrent['name'] = title[0].encode("utf-8")


        self.log(torrent['url']+"    "+torrent['name'])
        # print "书名：".decode("utf-8").encode("gbk") torrent['name']
        # print "价格:".decode("utf-8") + torrent['price']
        # print "会员价格:".decode("utf-8") + torrent['memprice']
        # print "链接:".decode("utf-8") + torrent['url']

        return torrent

        #
        #

        # torrent['description'] = x.select("//div[@id='description']").extract()
        # torrent['size'] = x.select("//div[@id='info-left']/p[2]/text()[2]").extract()
        #
        #
        # #self.make_requests_from_url(response.url).replace(callback=self.parse)
        # print 'Request=========================================', response.url
        #
        # #yield Request(response.url,callback=self.parse_torrent)
        #
        # #yield Request(response.url)
        #return torrent

        # name = 'myspider'
        # start_urls = (
        #     'http://example.com/page1',
        #     'http://example.com/page2',)
        # def parse(self, response):
        #     # collect `item_urls`
        #     for item_url in item_urls:
        #         yield Request(url=item_url, callback=self.parse_item)
        # def parse_item(self, response):
        #     item = MyItem()
        #     # populate `item` fields
        #     yield Request(url=item_details_url, meta={'item': item},
        #         callback=self.parse_details)
        # def parse_details(self, response):
        #     item = response.meta['item']
        #     # populate more `item` fields
        #     return item