# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from ..items import PracticumItem
# URL for front page of website
urls = 'http://voices.nationalgeographic.com/'


class BlogSpiderSpider(scrapy.Spider):
    name = 'nationalgeo'
    page_number = 2

    # Function to start spider
    def start_requests(self):
        yield scrapy.Request(url=urls,
                             callback=self.parse_front)

    # First parsing method
    def parse_front(self, response):
        # Path of article links
        article_links = response.xpath('//h3[@class="ng-text-edit-s ng-border-remove ng-padding-medium-bottom ng-margin-remove"]/a/@href')
        links_to_follow = article_links.extract()
        for link in links_to_follow:
            yield response.follow(url=link,
                                  callback=self.parse_pages)
        # Creates and calls front pages of website
        next_page = 'https://blog.nationalgeographic.org/page/' + str(BlogSpiderSpider.page_number) + '/'
        if BlogSpiderSpider.page_number <= 200:
            BlogSpiderSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse_front)

    def parse_pages(self, response):

        # calls the items.py file
        items = PracticumItem()
        # this will loop through multiple instances of specified tags in the url
        # this will allow multiple quotes to be extracted from the website
        # Due to no twitter link on site the twitter extract is empty
        twitter = []
        # extracts the article_date, author, article_text, and article_title of each blog
        article_date = response.xpath('//span[(@class="blog-meta-item blog-meta-date")]/time//text()').extract()
        article_title = response.xpath('//h3[(@class = "ng-entry-title ng-text-edit-m ng-padding-bottom-medium")]//text()').extract()
        author = response.xpath('//div[(@class="entry-contact-name")]//text()').extract()
        article_text = response.xpath('//div[(@class="has-content-area")]//text()').extract()
        # Cleans article_text
        body = ''
        for text in article_text:
            body = body + text
        # Error handling if certain extracts do not catch anything
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
        # Further cleans article_text
        body = body.replace('\r', '')
        body = body.replace('\n', '')
        body = body.replace('\t', '')
        # declares items extracted for each of the following
        items['article_url'] = response.request.url
        items['article_text'] = body
        items['timestamp'] = datetime.now()
        yield items
