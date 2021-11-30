import scrapy
from austmpdata.items import AustmpdataItem # We need this so that Python knows about the item object

class AustmpdataSpider(scrapy.Spider):
    name = 'austmpdata'  #The name of this spider

    # The allowed domain and the URLs where the spider should start crawling:
    allowed_domains = ['www.aph.gov.au']
    start_urls = ['http://www.aph.gov.au/Senators_and_Members/Parliamentarian_Search_Results?q=&mem=1&par=-1&gen=0&ps=0/']

    def parse(self, response):
        # The main method of the spider. It scrapes the URL(s) specified in the
        # 'start_url' argument above. The content of the scraped URL is passed on
        # as the 'response' object.

        nextpageurl = response.xpath("//a[@title='Next page']/@href")

        # When asked for a new item, ask self.scrape for new items and pass them along
        yield from self.scrape(response)

        if nextpageurl:
            path = nextpageurl.extract_first()
            nextpage = response.urljoin(path)
            print("Found url: {}".format(nextpage))
            yield scrapy.Request(nextpage, callback=self.parse)

    def scrape(self, response):
        for resource in response.xpath("//h4[@class='title']/.."):
            #Loop over each item on the page.
            item = AustmpdataItem() #Creating a new Item object

            item['name'] = resource.xpath("h4/a/text()").extract_first()

            # Instead of just writing the relative path of the profile page, lets make the full profile page so we
            # can use it later.
            profilepage = response.urljoin(resource.xpath("h4/a/@href").extract_first())
            item['link'] = profilepage

            item['district'] = resource.xpath("dl/dd/text()").extract_first()
            item['twitter'] = resource.xpath("dl/dd/a[contains(@class, 'twitter')]/@href").extract_first()
            item['party'] = resource.xpath("dl/dt[text()='Party']/following-sibling::dd/text()").extract_first()

            # We need to make a new variable that the scraper will return that will get passed through another callback.
            # We're calling that variable "request"
            request = scrapy.Request(profilepage, callback=self.get_phonenumber)
            request.meta['item'] = item #By calling .meta, we can pass our item object into the callback.
            yield request #Return the item + phonenumber back to the parser.

    def get_phonenumber(self, response):
        # A scraper designed to operate on one of the profile pages
        item = response.meta['item'] #Get the item we passed from scrape()
        item['phonenumber'] = response.xpath("//h3[text()='Electorate Office ']/following-sibling::dl/dd[1]/a/text()").extract_first()
        yield item #Return the new phonenumber'd item back to scrape










