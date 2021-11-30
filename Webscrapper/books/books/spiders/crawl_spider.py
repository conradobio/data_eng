import scrapy
#from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider#, Rule
from books.items import BooksItem


class CrawlSpiderSpider(CrawlSpider):
    name = 'crawl_spider'
    allowed_domains = ['books.toscrape.com']
    #start_urls = ['http://books.toscrape.com/']

    #rules = (
        #Rule(LinkExtractor(allow=r'catalogue/'), callback='parse_books', follow=True),)

    def start_requests(self):
        urls = ["http://books.toscrape.com/"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_pages)

    def parse_pages(self, response):
        #""" Using response.urljoin() to get individual book page """
        #books = response.xpath('//h3')
        #for book in books:
            #book_url = response.urljoin(book.xpath('.//a/@href').get())
            #yield scrapy.Request(url=book_url, callback=self.parse_books)


        #""" Using response.follow() to get individual book page"""
        books = response.xpath('//h3')
        for book in books:
            yield response.follow(url=book.xpath(".//a/@href").get(), callback=self.parse_books)

        #""" Using response. urljoin() to get next page """
        #next_page_url = response.xpath('//li[@class="next"]/a/@href').get()
        #if next_page_url is not None:
            # #next_page = response.urljoin(next_page_url)
            #yield scrapy.Request(url=next_page, callback=self.parse_pages)

        #    """ Using response.follow() to get next page """
        next_page_url = response.xpath('.//li[@class="next"]/a/@href').get()
        if next_page_url is not None:
            yield response.follow(url=next_page_url, callback=self.parse_pages)

    def parse_books(self, response):
        """ Filtering out pages other than books' pages to avoid getting "NotFound" error.
        Because, other pages would not have any 'div' tag with attribute 'class="col-sm-6 product_main"""

        title = response.xpath('//div[@class="col-sm-6 product_main"]/h1/text()').get()
        price = response.xpath('//div[@class="col-sm-6 product_main"]/p[@class="price_color"]/text()').get()
        stock = response.xpath('//div[@class="col-sm-6 product_main"]/p[@class="instock availability"]/text()').getall()[-1].strip()
        rating = response.xpath('//div[@class="col-sm-6 product_main"]/p[3]/@class').get()

        item = BooksItem()
        item['title'] = title
        item['price'] = price
        item['rating'] = rating
        item['stock'] = stock
        yield item