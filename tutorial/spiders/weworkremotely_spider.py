import scrapy
import re
from ..items import JobItem, JobLoader
from ..functions import iso_date2
from scrapy.loader.processors import TakeFirst
import uuid


class WeWorkRemotelySpider(scrapy.Spider):
    name = 'weworkremotely'
    start_urls = ['https://weworkremotely.com/#job-listings']
    

    def parse(self, response):
        
        #scrape info from website
        for job in response.css('li.feature'):
            
            # set up string for key word analysis
            job_title_str = job.css('span.title::text').get()
            job_desc_str = ''
            job_string = job_title_str + job_desc_str
            key_words = ['Intern', 'Entry Level', 'Entry-Level', 'Junior', 'Grad', 'Associate', 'Assistant']
            
            if any(x in job_string for x in key_words):
                l = JobLoader(item=JobItem(), selector=job)
                l.add_value('job_id', job.css('li > a').attrib['href'])
                l.add_css('job_position', 'span.title::text')
                l.add_css('company_name', 'span.company::text')
                l.add_value('job_location', 'Remote')
                l.add_value('job_salary', 'Not Available')
                l.add_value('job_description', job.css('span.region.company::text').get(default='Not Available'))
                l.add_value('published_at', iso_date2(job.css('time::text').get(default='Not Available')))
                l.add_value('application_link','www.weworkremotely.com{}'.format(job.css('li > a').attrib['href']))
                l.add_value('source','WeWorkRemotely.com')
                it = l.load_item()

                yield it            
            # if any(x in job_string for x in key_words):
            # job_id = 'None' #job.css('div').attrib['data-jk'],
            # job_position = job.css('span.title::text').get(),
            # company_name = job.css('span.company::text').get(),
            # job_location = 'Remote' #job.css('div.recJobLoc').attrib['data-rc-loc'],
            # job_salary = 'Follow link' #job.css('span.salaryText::text').get(),
            # job_description = 'Follow link' #job.css('p.job-result-card__snippet').get(),
            # published_at = job.css('time::text').get(),
            # application_link = 'www.weworkremotely.com{}'.format(job.css('li > a').attrib['href'])
            # source = 'WeWorkRemotely.com'
            
            
            
 
        
        # next_page = response.css('div.pagination')
        # next_page = next_page.css('a::attr(href)')[-1].get()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)