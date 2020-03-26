# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from ..items import PracticumItem
# URL for front page of website
urls = 'https://ourhealthandenvironment.wordpress.com/'


class BlogSpiderSpider(scrapy.Spider):
    name = 'ourhealth'
    page_number = 2

    def start_requests(self):
        yield scrapy.Request(url=urls,
                             callback=self.parse_front)

    # First parsing method
    def parse_front(self, response):
        # Path of article links
        article_links = response.xpath('//h1[@class="entry-title"]/a/@href')
        links_to_follow = article_links.extract()
        for link in links_to_follow:
            yield response.follow(url=link,
                                  callback=self.parse_pages)
        # Creates and calls front pages of website
        next_page = 'https://ourhealthandenvironment.wordpress.com/page/' + str(BlogSpiderSpider.page_number) + '/'
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
        # extracts the article_date, author, article_text, and article_title of each blogf]')
        article_date = response.xpath('//time[(@class="entry-date")]').re(r"\w+\s\d{1,2},\s\d{4}")
        article_title = response.xpath('//h1[(@class = "entry-title")]//text()').extract()
        author = response.xpath('//span[(@class="author vcard")]//text()').re(r"[A-Z]\w+\s\w+")
        article_text = response.xpath('//div[(@class="entry-content")]//text()').extract()
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
            two_authors = response.xpath('//span[@class = "submitted-by"]//text()').extract()
            items['author'] = two_authors[0]
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
