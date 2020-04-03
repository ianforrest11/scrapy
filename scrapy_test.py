import scrapy


class JobSpider(scrapy.Spider):
    name = 'jobs'
    page_number = 0
    start_urls = [
        'https://www.indeed.com/jobs?q=data+science&l=New+York,+NY&start='+ str(page_number) +'',
    ]

    def parse(self, response):
        for job in response.css('div.jobsearch-SerpJobCard'):
            yield {
                'job_id': job.css('div').attrib['id'],
                'job_title': job.css('a.jobtitle::text').extract(),
                'company': job.css('span.company::text').extract(),
                'location': job.css('div.accessible-contrast-color-location::text').extract(),
                'rating': job.css('span.ratingsContent::text').extract(),
                'date_posted': job.css('span.date::text').extract()
            }
        
        
        next_page = 'https://www.indeed.com/jobs?q=data+science&l=New+York,+NY&start='+ str(JobSpider.page_number) +''
        if JobSpider.page_number < 1093:
            JobSpider.page_number += 10
            yield response.follow(next_page, callback = self.parse)