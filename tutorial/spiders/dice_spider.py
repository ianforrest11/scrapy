# extracts info from

import scrapy
import re
from ..items import JobItem, JobLoader
from ..functions import iso_date
from scrapy.loader.processors import TakeFirst


class IndeedSpider(scrapy.Spider):
    name = 'dice'
    start_urls = ['https://www.dice.com/jobs?radius=30&radiusUnit=mi&page=1&pageSize=20&language=en']


    def parse(self, response):
        #scrape info from website
        for job in response.css('div.card'):

            # set up string for key word analysis
            job_title_str = job.css('h5 > a::text')
            job_desc_str = re.sub('<[^<]+?>', ' ', ''.join(job.css('div.summary li').getall()))
            job_string = job_title_str + job_desc_str
            key_words = ['Intern', 'Entry Level', 'Entry-Level', 'Junior', 'Grad', 'Associate', 'Assistant']
            
            if any(x in job_string for x in key_words):
                l = JobLoader(item=JobItem(), selector=job)
                l.add_value('job_id','None')
                l.add_value('job_position', 'h5 > a::text')
                #l.add_value('company_name', 'Not Available')
                l.add_value('company_name', 'Not Available')
                l.add_css('job_location', 'span::text')
                l.add_value('job_salary', 'Not Available')
                l.add_value('job_description', 'Not Available')
                #l.add_value('job_description', 'div.summary::text')
                l.add_value('published_at', 'Not Available')
                l.add_value('application_link','Not Available')
                l.add_value('source','Dice.com')
                it = l.load_item()

                yield it



        
        # next_page = response.css('ul.pagination')
        # next_page = next_page.css('li.pagination::attr(href)')[-1].get()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)