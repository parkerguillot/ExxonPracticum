# -*- coding: utf-8 -*-
import scrapy
from ..items import PracticumItem
urls = 'https://www.foe.org/blog/'


class FoeSpider(scrapy.Spider):
    name = 'foe'

    def start_requests(self):
        yield scrapy.Request(url=urls,
                             callback=self.parse_front)

    # First parsing method
    def parse_front(self, response, date):
        i = 0
        items = PracticumItem()
        article_date = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "col-md-8", " " ))]//time//text()').extract()
        print(article_date)
        next_page = response.css('.pager__item--next a::attr(href)').get()
        article_links = response.xpath('//strong[@class= "item-title"]/a/@href')
        print(article_links)
        links_to_follow = article_links.extract()
        for link in links_to_follow:
            date = article_date[i]
            i += 1
            yield date
            yield response.follow(url=link,
                                  callback=self.parse_pages)

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_front)

    def parse_pages(self, response):
        items = PracticumItem()
        twitter = []
        # response.xpath('//div[(@class="field field-name-field-twitter-id field-type-text field-label-hidden")]/a/@href]')
        # article_date = response.xpath('//time[@class = "entry-date published updated"]/text()').extract()
        article_title = response.xpath('//h1/text()').extract()
        author = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "post-author", " " ))]//text()').extract()
        article_text = response.xpath('//p/text()').extract()
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
            # if len(article_date) > 0:
            #     items['article_date'] = article_date[0]
            # else:
            #     items['article_date'] = ''
        if len(article_title) > 0:
            items['article_title'] = article_title[0]
        else:
            items['article_title'] = ''

        body = body.replace('\r', '')
        body = body.replace('\n', '')
        body = body.replace('\t', '')

            # declares items extracted for each of the following
        items['article_url'] = response.request.url
            # items['article_date'] = article_date
            # items['twitter'] = twitter
            # items['article_title'] = article_title
            # items['author'] = author
        items['article_text'] = body

        yield items