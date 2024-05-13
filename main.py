import scrapy
from scrapy.crawler import CrawlerProcess


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'quotes.json',
        'FEED_EXPORT_INDENT': 4,
        'FEED_EXPORT_ENCODING': 'utf-8',
    }


    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            yield {
                "tags": quote.xpath("div[@class='tags']/a/text()").extract(),
                "author": quote.xpath("span/small/text()").get(),
                "quote": quote.xpath("span[@class='text']/text()").get()
            }
        if next_link:= response.xpath("//li[@class='next']/a/@href").get():
            yield scrapy.Request(url=self.start_urls[0] + next_link)

class AuthorsSpider(scrapy.Spider):
    name = "authors"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'authors.json',
        'FEED_EXPORT_INDENT': 4,
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    def parse(self, response):

        author_links = response.css('.author + a::attr(href)').getall()
        for author_link in author_links:
            yield scrapy.Request(url=response.urljoin(author_link), callback=self.parse_author)
        
        if next_page:= response.css('li.next a::attr(href)').get():
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)
    
    def parse_author(self, response):
        yield {
            "fullname": response.css('.author-title::text').get(),
            "born_date": response.css('.author-born-date::text').get(),
            "born_location": response.css('.author-born-location::text').get(),
            "description": response.css('.author-description::text').get()
        }
        



if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.crawl(AuthorsSpider)
    process.start()