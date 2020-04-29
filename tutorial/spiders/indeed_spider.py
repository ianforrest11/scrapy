# extracts info from

import scrapy
import re
from ..items import JobItem, JobLoader
from ..functions import iso_date
from scrapy.loader.processors import TakeFirst


class IndeedSpider(scrapy.Spider):
    name = 'indeed'
    job_title = ''
    locations = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL',
               'GA', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA',
                'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE',
                 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI',
                  'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']
    key_words = ['Intern', 'Entry+Level', 'Entry-Level', 'Junior', 'Grad', 'Associate', 'Assistant', 'Staff']
    start_urls = []
    for job in key_words:
        for i in range(1,100):
            for location in locations:
                url = 'https://www.indeed.com/jobs?q={}&l={}&start={}'.format(job, location, i)
                start_urls.append(url)

    def parse(self, response):
        #scrape info from website
        for job in response.css('div.jobsearch-SerpJobCard'):
            l = JobLoader(item=JobItem(), selector=job)
            l.add_css('job_id','div::attr(data-jk)')
            l.add_css('job_position', 'a.jobtitle::attr(title)')
            l.add_value('company_name', job.css('span.company::text').get(default = 'Not Available'))
            l.add_value('company_name', job.css('span.company a.turnstileLink::text').get(default = 'Not Available'))
            l.add_css('job_location', 'div.recJobLoc::attr(data-rc-loc)')
            l.add_value('country', 'US')
            l.add_css('job_salary', 'span.salaryText::text')
            l.add_css('job_description', 'div.summary li::text')
            l.add_css('job_description', 'div.summary::text')
            l.add_value('published_at', iso_date(job.css('span.date::text').get()))
            l.add_value('application_link','www.indeed.com{}'.format(job.css('a.jobtitle').attrib['href']))
            l.add_value('source','Indeed.com')
            it = l.load_item()

            yield it
        
        next_page = response.css('div.pagination')
        next_page = next_page.css('a::attr(href)')[-1].get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)