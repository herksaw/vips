from scrapy.selector import HtmlXPathSelector
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor


DOMAIN = 'www.geckoandfly.com/'
URL = 'https://%s' % DOMAIN

url_list = []

class MySpider(Spider):
    name = DOMAIN
    allowed_domains = [DOMAIN]
    start_urls = [
        URL
    ]
    
    def parse(self, response):
        le = LinkExtractor() # empty for getting everything, check different options on documentation
        for link in le.extract_links(response):
            url_list.append(link.url)
            if len(url_list) > 50:
                break
            yield Request(link.url, callback=self.parse)
            

process = CrawlerProcess({
     'USER_AGENT': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",
        'DOWNLOAD_TIMEOUT':100,
        'REDIRECT_ENABLED':False,
        'SPIDER_MIDDLEWARES' : {
            'scrapy.spidermiddlewares.httperror.HttpErrorMiddleware':True
        }
})

process.crawl(MySpider)
process.start()

for url in url_list:
    print(url)