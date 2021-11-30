import scrapy
from ukparl.items import UkparlItem

class UkparlSpider(scrapy.Spider):
    name = 'ukparldata'
    #allowed_domains = ["members.parliament.uk/"]
    start_urls = ['https://members.parliament.uk/members/commons?page=1']

    def parse(self, response):
        nextpageurl = response.xpath('//a[@title="Go to next page"]/@href')
        yield from self.scrape(response)

        if nextpageurl:
            path = nextpageurl.extract_first()
            nextpage = response.urljoin(path)
            print("Found url: {}".format(nextpage))
            yield scrapy.Request(nextpage)

    def scrape(self, response):
        for resource in response.xpath('//div[@class="primary-info"]/..'):
            item = UkparlItem()

            item['name'] = resource.xpath('div[@class="primary-info"]/text()').extract_first().strip()

            profilepage = response.urljoin(resource.xpath('../../@href').extract_first())
            item['link'] = profilepage
            item['party'] = resource.xpath('div[@class="secondary-info"]/text()').extract_first().strip()
            item['region'] = resource.xpath('//div[@class="indicator indicator-label"]/text()').extract_first().strip()

            request = scrapy.Request(profilepage, callback=self.get_data)
            request.meta['item'] = item
            yield request

    def get_data(self, response):
        item = response.meta['item']
        item['phonenumber'] = response.xpath('//div[@class="contact-line"]/a/text()').extract_first().strip()
        item['twitter'] = response.xpath('//a[contains(.,"twitter")]/@href').extract_first()
        yield item
