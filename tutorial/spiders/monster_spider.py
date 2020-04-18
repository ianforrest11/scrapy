# extracts info from

import scrapy
import re
from ..items import JobItem, JobLoader
from ..functions import iso_date
from scrapy.loader.processors import TakeFirst


class MonsterSpider(scrapy.Spider):  
    name = 'monster'
    locations = 'NY' #['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL',
    #             'GA', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA',
    #             'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE',
    #             'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI',
    #             'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']   
    start_urls = ['https://www.monster.com/jobs/search/?where=&stpage=1&page=%s' % page for page in range(1,100)]
    
    # for location in locations:
    #     url = ('https://www.monster.com/jobs/search/?where='+ location.replace(" ", "+") +'&stpage=0&page=%s' % page for page in xrange(1,54))
    #     start_urls.append(url)   


    def parse(self, response):
        #scrape info from website
        for job in response.css('section.card-content'):

            # TODO set up string for key word analysis
            job_title_str = job.css('a::text').get()
            key_words = ['Intern', 'Entry Level', 'Entry-Level', 'Junior', 'Grad', 'Associate', 'Assistant', 'Staff']

            if any(x in job_title_str for x in key_words):
                l = JobLoader(item=JobItem(), selector=job)
                #l.add_xpath('job_id','')
                l.add_css('job_id', 'section.card-content::attr(data-jobid)')
                l.add_css('job_id', 'h2.title a::attr(href)')
                l.add_css('job_position', 'a::text')
                #l.add_value('company_name', 'Not Available')
                l.add_css('company_name', 'div.company span.name::text')
                l.add_css('job_location', 'div.location span.name::text')
                l.add_value('job_salary', 'Not Available')
                l.add_value('job_description', 'Not Available')
                #l.add_value('job_description', 'div.summary::text')
                l.add_value('published_at', iso_date(job.css('div.meta time::text').get(default = 'Not Available')))
                l.add_css('application_link','h2.title a::attr(href)')
                l.add_value('source','Monster.com')
                it = l.load_item()

                yield it


        # # TODO fix pagination
        # next_page = response.css('a.mux-btn::attr(href)').get()
        # #next_page = next_page.css('a.mux-btn::attr(href)').get()
        # if next_page is not None:
        #     #next_page = response.follow(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)