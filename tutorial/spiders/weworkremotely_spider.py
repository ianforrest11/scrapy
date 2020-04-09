import scrapy
import re
from ..items import JobItem


class WeWorkRemotelySpider(scrapy.Spider):
    name = 'weworkremotely'
    start_urls = ['https://weworkremotely.com/#job-listings']
    

    def parse(self, response):
        
        items = JobItem()
        
        #scrape info from website
        for job in response.css('li.feature'):
            
            # set up string for key word analysis
            # job_title_str = job.css('span.title::text').get()
            # job_desc_str = ''
            # job_string = job_title_str + job_desc_str
            # key_words = ['Intern', 'Entry Level', 'Entry-Level', 'Junior', 'Grad']
            
            # if any(x in job_string for x in key_words):
            job_id = 'None' #job.css('div').attrib['data-jk'],
            job_position = job.css('span.title::text').get(),
            company_name = job.css('span.company::text').get(),
            job_location = 'Remote' #job.css('div.recJobLoc').attrib['data-rc-loc'],
            job_salary = 'Follow link' #job.css('span.salaryText::text').get(),
            job_description = 'Follow link' #job.css('p.job-result-card__snippet').get(),
            published_at = job.css('time::text').get(),
            application_link = 'www.weworkremotely.com{}'.format(job.css('li > a').attrib['href'])
            source = 'WeWorkRemotely.com'

            #convert to item object
            items['job_id'] = job_id
            items['job_position'] = job_position
            items['company_name'] = company_name
            items['job_location'] = job_location
            items['job_salary'] = job_salary
            items['job_description'] = job_description
            items['published_at'] = published_at
            items['application_link'] = application_link
            items['source'] = source
            
            
            
            yield items
        
        # next_page = response.css('div.pagination')
        # next_page = next_page.css('a::attr(href)')[-1].get()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)