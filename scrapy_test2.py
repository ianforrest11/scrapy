## goes within each job page (from main pages) and extracts info

import scrapy


class JobSpider(scrapy.Spider):
    name = 'jobs2'

    start_urls = ['https://www.indeed.com/q-data-science-l-New-York,-NY-jobs.html']

    def parse(self, response):
        job_page_links = response.css('.jobtitle')
        yield from response.follow_all(job_page_links, self.parse_job)

        pagination_links = response.css('div.pagination a')
        yield from response.follow_all(pagination_links, self.parse)

    def parse_job(self, response):
        def extract_with_css(query):
            print(response.css(query).get(default='').strip())
            return response.css(query).get(default='').strip()
            

        yield {
            'job_title': extract_with_css('h3.jobsearch-JobInfoHeader-title::text'),
            'company': extract_with_css("div.jobsearch-JobInfoHeader-companyNameAndReview::text"),
            'location': extract_with_css("div.jobsearch-JobInfoHeader-companyLocation span::text")
            }

