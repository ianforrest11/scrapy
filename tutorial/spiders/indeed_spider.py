# extracts info from

import scrapy
import re
from scrapy.loader import ItemLoader
from ..items import JobItem
from ..functions import iso_date, parse


class IndeedSpider(scrapy.Spider):
    name = 'indeed'
    job_title = ''
    locations = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL',
               'GA', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA',
                'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE',
                 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI',
                  'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']
    start_urls = []
    
    for location in locations:
        url = 'https://www.indeed.com/jobs?q='+ job_title.replace(" ", "+") +'&l='+ location.replace(" ", "+") +'&start=0'
        start_urls.append(url)

    def parse(self, response):
        
        items = JobItem()
        
        #scrape info from website
        for job in response.css('div.jobsearch-SerpJobCard'):
            
            # set up string for key word analysis
            job_title_str = job.css('a.jobtitle').attrib['title']
            job_desc_str = re.sub('<[^<]+?>', ' ', ''.join(job.css('div.summary li').getall()))
            job_string = job_title_str + job_desc_str
            key_words = ['Intern', 'Entry Level', 'Entry-Level', 'Junior', 'Grad']
            #''.join(item.xpath('li[@class="desc"]//text()').extract())
            if any(x in job_string for x in key_words):
                job_id =  job.css('div').attrib['data-jk'],
                job_position = job.css('a.jobtitle').attrib['title'],
                company_name = job.css('span.company a.turnstileLink::text').get(),
                job_location = job.css('div.recJobLoc').attrib['data-rc-loc'],
                job_salary = job.css('span.salaryText::text').get(),
                job_description = re.sub('<[^<]+?>', ' ', ''.join(job.css('div.summary li').getall())),
                published_at = iso_date(job.css('span.date::text').get()),
                application_link = 'www.indeed.com{}'.format(job.css('a.jobtitle').attrib['href'])
                source = 'Indeed.com'

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
                
                for item in items:
                    ''.join(item)
                
                yield items
        
        next_page = response.css('div.pagination')
        next_page = next_page.css('a::attr(href)')[-1].get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)