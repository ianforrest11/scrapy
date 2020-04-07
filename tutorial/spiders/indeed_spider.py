# extracts info from

import scrapy
import re
from ..items import JobItem


class JobSpider(scrapy.Spider):
    name = 'indeed'
    page_number = 0
    job_title = ''
    location = 'NY'
    start_urls = [
        'https://www.indeed.com/jobs?q='+ job_title.replace(" ", "+") +'&l='+ location.replace(" ", "+") +'&start='+ str(page_number) +'',
    ]

    def parse(self, response):
        
        items = JobItem()
        
        #scrape info from website
        for job in response.css('div.jobsearch-SerpJobCard'):
            job_id =  job.css('div').attrib['data-jk'],
            job_title = job.css('a.jobtitle').attrib['title'],
            company = job.css('span.company a.turnstileLink::text').get(),
            location = job.css('div.recJobLoc').attrib['data-rc-loc'],
            salary = job.css('span.salaryText::text').get(),               
            rating = job.css('span.ratingsContent::text').get(),
            job_desc = re.sub('<[^<]+?>', ' ', ''.join(job.css('div.summary li').getall())),
            date_posted = job.css('span.date::text').get(),
            link = 'www.indeed.com{}'.format(job.css('a.jobtitle').attrib['href'])
            
            #convert to item object
            items['job_id'] = job_id
            items['job_title'] = job_title
            items['company'] = company
            items['location'] = location
            items['salary'] = salary
            items['rating'] = rating
            items['job_desc'] = job_desc
            items['date_posted'] = date_posted
            items['link'] = link
            
            
            
            yield items
        
        next_page = response.css('div.pagination')
        next_page = next_page.css('a::attr(href)')[-1].get()
        print(next_page)
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)