# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from ..items import PracticumItem
# URL for frontpage of website
urls = 'https://www.rwjf.org/en/blog.html'


class BlogSpiderSpider(scrapy.Spider):
    name = 'rwjf'

    # Function to start spider
    def start_requests(self):
        yield scrapy.Request(url=urls,
                             callback=self.parse_front)

    # First parsing method
    def parse_front(self, response):
        # Path of the next page
        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        # Path of article links
        article_links = response.xpath('//div[@class="post-content"]/h2/a/@href')
        links_to_follow = article_links.extract()
        for link in links_to_follow:
            yield response.follow(url=link,
                                  callback=self.parse_pages)
        # URL is included in yield because next page path does not get the first part of the url
        if next_page is not None:
            yield response.follow('https://www.rwjf.org/' + next_page, callback=self.parse_front)


    def parse_pages(self, response):

        # calls the items.py file
        items = PracticumItem()
        # this will loop through multiple instances of specified tags in the url
        # this will allow multiple quotes to be extracted from the website
        # Due to no twitter link on site the twitter extract is empty
        twitter = []
        # extracts the article_date, author, article_text, and article_title of each blog
        article_date = response.xpath('//div[(@class="post-content")]').re(r"\w+\s\d{1,2},\s\d{4}")
        article_title = response.xpath('//h1[(@class = "post-title")]//text()').extract()
        author = response.xpath('//span[contains(@itemprop, "name")]/a//text()').extract()
        article_text = response.xpath('//div[(@class="rwjf-component rwjf-blog-freeform section")]//text()').extract()
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
        items['article_date'] = article_date
        items['twitter'] = twitter
        items['article_title'] = article_title
        items['author'] = author
        items['article_text'] = body
        items['timestamp'] = datetime.now()
        yield items