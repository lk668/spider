#!/usr/bin/python
# -*- coding:utf-8 -*-

# from scrapy.contrib.spiders import  CrawlSpider,Rule

from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from company.items import CompanyItem

length = 0
class CompanySpider(Spider):
    """爬虫CompanySpider"""
    name = "Company"

    #减慢爬取速度 为0.5s
    download_delay = 0.5
    allowed_domains = ['ecp.sgcc.com.cn']
    start_urls = [
        #第一页地址
        "http://ecp.sgcc.com.cn/news_list.jsp?site=global&column_code=014002003&company_id=01&news_name=all&pageNo=1",
    ]
    for i in range(2,4):
        start_urls.append("http://ecp.sgcc.com.cn/news_list.jsp?site=global&column_code=014002003&company_id=01&news_name=all&pageNo=" + str(i))
    def parse(self, response):
        sel = Selector(response)
        news_url=[]
        #items = []
        #获得新闻url和标题
        item = CompanyItem()
        urls = sel.xpath('//div[@class="titleList"]/ul[@class="newslist01"]/li/a/@onclick').extract()
        for url in urls:
            news_url.append("http://ecp.sgcc.com.cn/html/news/014002003/"+url[29:-3]+".html")
        news_name = sel.xpath('//div[@class="titleList"]/ul[@class="newslist01"]/li/a/@title').extract()

        for i in range(0,len(news_name)):
            yield Request(news_url[i].encode('utf-8'), callback = self.parse_cpy)

    def parse_cpy(self, response):
        sel = Selector(response)
        item = CompanyItem()
        item['news_name']= sel.xpath('//head/title/text()').extract()[0]
        item['news_url'] = response.url
        cpy = []
        k = ""
        item['news_content'] = []
        num = sel.xpath('//tbody/tr/td/@width').extract()
        if len(num) > 0:
            for n in num:
                if int(n) > 160:
                    k = n
                    break
            if k!="":
                print "^^^^^^^^^^^^^^^^^^^"
                cpy = sel.xpath('//tbody/tr/td[@width = %s]/p/font/span/text()'%k).extract()
                if len(cpy) > 0:
                    #print cpy
                    print "&&&&&&&&&&&"
                    for comp in cpy:
                        item['news_content'].append(comp.encode('utf-8'))
                else:
                    cpy = sel.xpath('//tbody/tr/td[@width = %s]/p/span/text()'%k).extract()
                    print "&&&&&&&&&&&"
                    for comp in cpy:
                        item['news_content'].append(comp.encode('utf-8'))
        yield item
