# extracts info from

import scrapy
import re


class JobSpider(scrapy.Spider):
    name = 'jobs'
    page_number = 0
    job_title = 'cleaner'
    location = ''
    start_urls = [
        'https://www.indeed.com/jobs?q='+ job_title.replace(" ", "+") +'&l='+ location.replace(" ", "+") +'&start='+ str(page_number) +'',
    ]

    def parse(self, response):
        for job in response.css('div.jobsearch-SerpJobCard'):
            yield {
                'job_id': job.css('div').attrib['data-jk'],
                'job_title': job.css('a.jobtitle').attrib['title'],
                'company': job.css('span.company a.turnstileLink::text').get(),
                'location': job.css('div.recJobLoc').attrib['data-rc-loc'],
                'salary': job.css('span.salaryText::text').get(),               
                'rating': job.css('span.ratingsContent::text').get(),
                'job_desc': re.sub('<[^<]+?>', ' ', ''.join(job.css('div.summary li').getall())),
                'date_posted': job.css('span.date::text').get(),
                'link': 'www.indeed.com{}'.format(job.css('a.jobtitle').attrib['href'])
            }
        
        next_page = response.css('div.pagination')
        next_page = next_page.css('a::attr(href)')[5].get()
        print('NEXT PAGEEEEEEEEEEE', next_page)
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        
        # next_page = 'https://www.indeed.com/jobs?q='+ job_title.replace(" ", "+") +'&start='+ str(JobSpider.page_number) +''
        # if JobSpider.page_number < 1093:
        #     JobSpider.page_number += 10
        #     yield response.follow(next_page, callback = self.parse)