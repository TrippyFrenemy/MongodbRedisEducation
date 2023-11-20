import scrapy
import json
from ..items import QuoteItem, AuthorItem
from ..pipelines import JsonWriterPipeline


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['http://quotes.toscrape.com']
    custom_settings = {"ITEM_PIPELINES": {JsonWriterPipeline: 300}}

    def parse(self, response):
        for quote in response.css('div.quote'):
            quote_text = quote.css('span.text::text').get()
            author_name = quote.xpath('span/small/text()').get()
            tags = quote.css('div.tags a.tag::text').getall()
            author_page = quote.xpath('span/a/@href').get()

            quote_item = QuoteItem()
            quote_item['quote'] = quote_text
            quote_item['author'] = author_name
            quote_item['tags'] = tags

            yield response.follow(url=self.start_urls[0] + quote.xpath("span/a/@href").get(),
                                  callback=self.parse_author)

            yield quote_item

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_author(self, response):
        author_item = AuthorItem()
        author_item['fullname'] = response.css('h3.author-title::text').get().strip()
        author_item['born_date'] = response.css('span.author-born-date::text').get().strip()
        author_item['born_location'] = response.css('span.author-born-location::text').get().strip()
        author_item['description'] = response.css('div.author-description::text').get().strip()

        yield author_item
