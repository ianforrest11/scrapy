import scrapy

class JobSpider(scrapy.Spider):
    name = 'jobs'
    start_urls = [
        'https://entrylevel.io/',
    ]

    def parse(self, response):
        for job in response.css('ul.job-list'):
            yield {
                #'title': quote.xpath('span/small/text()').get(),
                'title': job.xpath('h1/text()').get(),
                #'text': quote.css('span.text::text').get(),
                'location': job.css('p[1]/text()').get(),
            }