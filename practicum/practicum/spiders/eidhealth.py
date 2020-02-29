# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
from ..items import PracticumItem
from datetime import datetime
# urls = list of urls that will be used in the model

urls = 'https://eidhealth.org/category/blog/'


class EIDSpider(scrapy.Spider):
    # name = declaring the name of spider for later use in program
    name = 'eidhealth'

    def start_requests(self):
        yield scrapy.Request(url=urls,
                             callback=self.parse_front)

    # First parsing method
    def parse_front(self, response):
        next_page = response.xpath('//a[@class = "next page-numbers"]/@href').get()
        article_links = response.xpath('//h2[@class = "cat-headline"]/a/@href')
        links_to_follow = article_links.extract()
        for link in links_to_follow:
            yield response.follow(url=link,
                                  callback=self.parse_pages)

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_front)

    def parse_pages(self,response):

        # calls the items.py file
        items = PracticumItem()

        twitter = []
# response.xpath('//div[(@class="field field-name-field-twitter-id field-type-text field-label-hidden")]/a/@href]')
        article_date = response.xpath('//div[@class = "meta"]//p//text()').re(r"\w+\s\d{1,2},\s\d{4}")
        article_title = response.xpath('//h1[(@class = "feature-story-h1")]//text()').extract()
        author = response.xpath('//div[@class = "meta"]//p//text()').re(r"[A-Z]\w+\s\w+")
        article_text = response.xpath('//p//text()').extract()
        body = ''
        for text in article_text:
            body = body + text
        if len(twitter) > 0:
            items['twitter'] = twitter[0]
        else:
            items['twitter'] = ''
        if len(author) > 0:
            items['author'] = author[0]
        else:
            items['author'] = ''
        if len(article_date) > 0:
            items['article_date'] = article_date[0]
        else:
            items['article_date'] = ''
        if len(article_date) > 0:
            items['article_title'] = article_title[0]
        else:
            items['article_title'] = ''
            # article_title = article_title.replace('\r', '')
            # article_title = article_title.replace('\n', '')
            # article_title = article_title.replace('\t', '')
        body = body.replace('\r', '')
        body = body.replace('\n', '')
        body = body.replace('\t', '')
            # region = region.replace('\r', '')
            # region = region.replace('\n', '')
            # region = region.replace('\t', '')
            # author = author.replace('\r', '')
            # author = author.replace('\n', '')
            # author = author.replace('\t', '')

            # declares items extracted for each of the following
        items['article_url'] = response.request.url
            # items['article_date'] = article_date
            # items['twitter'] = twitter
            # items['article_title'] = article_title
            # items['author'] = author
        items['article_text'] = body
        items['timestamp'] = datetime.now()

        yield items

        # this assigns a value for looking at pagination in a url
        # next_page = response.css('li.next a::attr(href)') .get()
        # next_page = response.css('li.next.next_last a::attr(href)').get()

        # if condition to check if next_page value is empty or there are no more pages to comb through
        # if next_page is not None:
        # if next_page is not None:
        #    yield response.follow(next_page, callback=self.parse_front)




