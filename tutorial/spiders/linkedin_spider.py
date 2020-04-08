import scrapy
import re
from ..items import JobItem


class JobSpider(scrapy.Spider):
    name = 'linkedin'
    job_title = ''
    locations = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL',
               'GA', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA',
                'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE',
                 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI',
                  'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']
    start_urls = []
    
    for location in locations:
        url = 'https://www.linkedin.com/jobs/search?keywords='+ job_title.replace(" ", "+") +'&location='+ location.replace(" ", "+") +'&trk=homepage-basic_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0'
        start_urls.append(url)

    def parse(self, response):
        
        items = JobItem()
        
        #scrape info from website
        for job in response.css('li.result-card'):
            
            # set up string for key word analysis
            job_title_str = job.css('h3.result-card__title::text').get()
            job_desc_str = job.css('p.job-result-card__snippet').get()
            job_string = job_title_str + job_desc_str
            key_words = ['Intern', 'Entry Level', 'Entry-Level', 'Junior', 'Grad']
            
            if any(x in job_string for x in key_words):
                job_id = '' #job.css('div').attrib['data-jk'],
                job_position = job.css('h3.result-card__title::text').get(),
                company_name = '' #job.css('span.company a.turnstileLink::text').get(),
                job_location = '' #job.css('div.recJobLoc').attrib['data-rc-loc'],
                job_salary = '' #job.css('span.salaryText::text').get(),
                job_description = job.css('p.job-result-card__snippet').get(),
                published_at = '' #job.css('span.date::text').get(),
                application_link = '' #'www.indeed.com{}'.format(job.css('a.jobtitle').attrib['href'])
                source = 'LinkedIn.com'
                
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
        
        next_page = response.css('div.pagination')
        next_page = next_page.css('a::attr(href)')[-1].get()
        print(next_page)
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)