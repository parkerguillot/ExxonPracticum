# -*- coding: utf-8 -*-
import scrapy
from ..items import ExxonItem
from datetime import datetime

urls = 'http://thetoxicologisttoday.blogspot.com/'


class SpideySensesAreTingling(scrapy.Spider):
        name = 'toxictoday'

        def start_requests(self):
            yield scrapy.Request(url=urls,
                                 callback=self.parse_front)

        # First parsing method
        def parse_front(self, response):
            next_page = response.xpath('//a[contains(@class, "older")]//@href').get()
            print(next_page)
            article_links = response.xpath('//h3[@class = "post-title entry-title"]/a/@href')
            print(article_links)
            links_to_follow = article_links.extract()
            for link in links_to_follow:
                yield response.follow(url=link,
                                      callback=self.parse_pages)

            if next_page is not None:
                yield response.follow(next_page, callback=self.parse_front)

        def parse_pages(self, response):

            # calls the items.py file
            items = ExxonItem()

            # looks at source code but only at a certain html tag in the document
            # html tag for quotes is the div (tag) which is why it is specified first

            # this will loop through multiple instances of specified tags in the url
            # this will allow multiple quotes to be extracted from the website
            # extracts the region, article_date, and article_title of each blog
            twitter = []
            # response.xpath('//div[(@class="field field-name-field-twitter-id field-type-text field-label-hidden")]/a/@href]')
            article_date = response.xpath('//h2[@class = "date-header"]//text()').extract()
            article_title = response.xpath('//h3[@class = "post-title entry-title"]//text()').extract()
            author = response.xpath('//span[@itemprop = "name"]/text()').extract()
            article_text = response.xpath('//div[@style = "text-align: justify;"]//text()').extract()
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