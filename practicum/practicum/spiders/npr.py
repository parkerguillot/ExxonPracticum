# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
import re
from ..items import PracticumItem
from datetime import datetime
# urls = list of urls that will be used in the model

urls = 'https://www.npr.org/sections/health-shots/'
# Each Spider will perform a different function when extracting information


class NprSpider(scrapy.Spider):
    # name = declaring the name of spider for later use in program
    name = 'Npr'
    count = 1

    def start_requests(self):
        yield scrapy.Request(url=urls,
                             callback=self.parse_front)

    # First parsing method
    def parse_front(self, response):

        # next_page = response.xpath('//li[contains(@class, "next")]/a/@href').get()
        article_links = response.xpath('//h2[@class = "title"]/a/@href')
        links_to_follow = article_links.extract()
        for link in links_to_follow:
            NprSpider.count += 1
            yield response.follow(url=link,
                                  callback=self.parse_pages)

        for c in range(100):
            page = c + 2
            params = {'start': NprSpider.count
                     }
            print('PAGE NUMBER >>>>>>', page, '!!!!!')
            conturl = 'https://www.npr.org/sections/health-shots/'
            yield scrapy.FormRequest(url=conturl, method='GET', formdata=params, callback=self.parse_front)

    def parse_pages(self, response):

        # calls the items.py file
        items = PracticumItem()

        # looks at source code but only at a certain html tag in the document
        # html tag for quotes is the div (tag) which is why it is specified first
        # all_blogs = response.css('main.content')

        # this will loop through multiple instances of specified tags in the url
        # this will allow multiple quotes to be extracted from the website
        # extracts the region, article_date, and article_title of each blog
        # for blogs in all_blogs:
        article_date = response.xpath('//span[@class = "date"]//text()').re(r"\w+\s\d{1,2},\s\d{4}")
        article_title = response.xpath('//h1//text()').extract()
        author = response.xpath('//a[@rel = "author"]/text()').re(r"[A-Z]\w+\s\w+")
        article_text = response.xpath('//p//text()').extract()
        twitter = []  # response.xpath('//a[@class = "contactLink expert-twitter-follow"]/@href').extract()
        # if article_date = None:
        #     article_date = 'Null'
        # twitter = 'no twitter'
        if len(twitter) > 0:
            items['twitter'] = twitter[0]
        else:
            items['twitter'] = ''
        body = ''
        for text in article_text:
            body = body + text
        if len(article_date) > 0:
            items['article_date'] = article_date[0]
        else:
            items['article_date'] = ''
        if len(article_title) > 0:
            items['article_title'] = article_title[0]
        else:
            items['article_title'] = ''
        if len(author) > 0:
            items['author'] = author[0]
        else:
            items['author'] = ''
            # # blog_title = ''
            # # for title in article_title:
            # #     blog_title = blog_title + title
            # blog_region = ''
            # for area in region:
            #     blog_region = blog_region + area
            # # blog_title = blog_title.replace('\r', '')
            # # blog_title = blog_title.replace('\n', '')
            # # blog_title = blog_title.replace('\t', '')
            # body = body.replace('\r', '')
            # body = body.replace('\n', '')
            # body = body.replace('\t', '')
            # blog_region = blog_region.replace('\r', '')
            # blog_region = blog_region.replace('\n', '')
            # blog_region = blog_region.replace('\t', '')


            # declares items extracted for each of the following
        items['article_url'] = response.request.url
        # items['article_date'] = article_date[0]
        # items['article_title'] = article_title
        # items['author'] = author
        items['article_text'] = body
        items['timestamp'] = datetime.now()
        # items['twitter'] = twitter

        yield items

        # this assigns a value for looking at pagination in a url
        # next_page = response.css('li.next a::attr(href)') .get()
        # next_page = response.css('li.next.next_last a::attr(href)').get()