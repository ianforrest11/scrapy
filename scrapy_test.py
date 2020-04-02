import scrapy


class JobSpider(scrapy.Spider):
    name = 'jobs'
    page_number = 10
    start_urls = [
        'https://www.indeed.com/jobs?q=data+science&l=New+York,+NY&start=0',
    ]

    def parse(self, response):
        for job in response.css('div.jobsearch-SerpJobCard'):
            yield {
                'job_id': job.css('div.SerpJobCard::attr("id")').extract(),
                'job_title': job.css('a.jobtitle::text').extract(),
                'company': job.css('span.company::text').extract(),
                'location': job.css('div.accessible-contrast-color-location::text').extract(),
                'rating': job.css('span.ratingsContent::text').extract(),
                'date_posted': job.css('span.date::text').extract()
            }
        
        next_page = 'https://www.indeed.com/jobs?q=data+science&l=New+York,+NY&start='+ str(JobSpider.page_number) +''
        JobSpider.page_number += 10
        if JobSpider.page_number < 1093:
            yield response.follow(next_page, callback = self.parse)
        