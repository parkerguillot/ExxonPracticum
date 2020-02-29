# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from ..items import PracticumItem
urls = 'http://healthpolicyandmarket.blogspot.com/'


class HealthPolicySpider(scrapy.Spider):
    name = 'healthpolicy'
    # establish the earliest blogs we would like to scrape
    year = 2012

    def start_requests(self):
        yield scrapy.Request(url= urls,
                             callback=self.pages)

    def pages(self,response):
        start_url = 'http://healthpolicyandmarket.blogspot.com/' + str(HealthPolicySpider.year) + '/'
        yield response.follow(start_url, callback=self.parse_front)

    def parse_front(self, response):
        article_links = response.xpath('//h3[@class="post-title entry-title"]/a/@href')
        links_to_follow = article_links.extract()
        for link in links_to_follow:
            yield response.follow(url=link,
                                  callback=self.parse_pages)

        if HealthPolicySpider.year < 2020:
            HealthPolicySpider.year += 1
            next_page = 'http://healthpolicyandmarket.blogspot.com/' + str(HealthPolicySpider.year) + '/'
            print(HealthPolicySpider.year)
            yield response.follow(next_page, callback=self.parse_front)

    def parse_pages(self, response):

        # calls the items.py file
        items = PracticumItem()

        # looks at source code but only at a certain html tag in the document
        # html tag for quotes is the div (tag) which is why it is specified first

        # this will loop through multiple instances of specified tags in the url
        # this will allow multiple quotes to be extracted from the website
        # extracts the region, article_date, and article_title of each blog
        twitter = []
# response.xpath('//div[(@class="field field-name-field-twitter-id field-type-text field-label-hidden")]/a/@href]')
        article_date = response.xpath('//h2[(@class="date-header")]').re(r"\w+\s\d{1,2},\s\d{4}")
        article_title = response.xpath('//h3[(@class = "post-title entry-title")]//text()').extract()
        author = response.xpath('//span[(@itemprop="name")]//text()').re(r"[A-Z]\w+\s\w+")
        article_text = response.xpath('//div[(@class="post-body entry-content")]//text()').extract()
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
            items['article_title'] = article_title[0]
        else:
            items['article_title'] = ''
        body = body.replace('\r', '')
        body = body.replace('\n', '')
        body = body.replace('\t', '')

        # declares items extracted for each of the following
        items['article_url'] = response.request.url
        items['article_date'] = article_date[0]
        # items['twitter'] = twitter
        # items['article_title'] = article_title
        # items['author'] = author
        items['article_text'] = body
        items['timestamp'] = datetime.now()

        yield items