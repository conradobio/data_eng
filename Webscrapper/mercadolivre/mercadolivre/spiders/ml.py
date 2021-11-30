import scrapy

class MlSpider(scrapy.Spider):
    name = 'ml'
    start_urls = ["https://celulares.mercadolivre.com.br"]

    def parse(self, response, **kwargs):
        for i in response.xpath('//li[@class="ui-search-layout__item"]'):
            price = i.xpath('.//div[@class ="ui-search-price__second-line"]//span[@class="price-tag-fraction"]/text()').get()
            title = i.xpath('.//h2[@class="ui-search-item__title"]//text()').get()
            link = i.xpath('.//a/@href').get()
            brand = title.split(' ')[0]

            yield {
                'price' : price,
                'title' : title,
                'link' : link
            }

            #next_page = response.xpath("//a[contains(@title,'Seguinte')]/@href").get()
            #next_page = response.xpath("//a[contains(@title,"Próximo")]/@href").get()

            #if next_page:
            #    yield scrapy.Request(url=next_page, callback=self.parse)

