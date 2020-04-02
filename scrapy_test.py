import scrapy


class JobSpider(scrapy.Spider):
    name = 'jobs'
    start_urls = [
        'https://www.indeed.com/q-data-science-l-New-York,-NY-jobs.html',
    ]

    def parse(self, response):
        for job in response.css('div.jobsearch-SerpJobCard'):
            yield {
                'job_title': job.css('a.jobtitle::text').extract(),
                'company': job.css('span.company::text').extract(),
                'location': job.css('div.accessible-contrast-color-location::text').extract(),
                'rating': job.css('span.ratingsContent::text').extract()
            }
        
        next_page = response.css('div.pagination a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
        