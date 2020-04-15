# extracts info from

import scrapy
import re
from ..items import JobItem, JobLoader
from ..functions import iso_date, parse
from scrapy.loader.processors import TakeFirst


class IndeedSpider(scrapy.Spider):
    name = 'indeed2'
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
        #scrape info from website
        for job in response.css('div.jobsearch-SerpJobCard'):
            
            # set up string for key word analysis
            job_title_str = job.css('a.jobtitle').attrib['title']
            job_desc_str = re.sub('<[^<]+?>', ' ', ''.join(job.css('div.summary li').getall()))
            job_string = job_title_str + job_desc_str
            key_words = ['Intern', 'Entry Level', 'Entry-Level', 'Junior', 'Grad']
            #''.join(item.xpath('li[@class="desc"]//text()').extract())
            if any(x in job_string for x in key_words):
                il = JobLoader(response=response)
                il.selector = response.xpath('(//address)[1]')

                il.add_xpath('city', './/span[@class="locality"]/text()')
                il.add_xpath('address', 'div[@class="street-address"]/text()',
                            lambda x: [s.strip() for s in x])
                if self.meta_country in response.meta:
                    il.add_value('country', response.meta[self.meta_country])
                    if il.get_collected_values('country')[0] in self.hours_countries:
                        il.add_value('hours',
                                    il.selector.xpath(
                                        '../table[@class="store-info"][1]/tr'),
                                    self.parse_hours)
                il.add_xpath('phone_number', 'div[@class="telephone-number"]/text()',
                            TakeFirst(), unicode.strip)
                il.add_xpath('services',
                            '//nav[@class="nav hero-nav selfclear"]//img/@alt')
                il.add_xpath('state', './/span[@class="region"]/text()', TakeFirst())
                # store_email: not found
                # store_floor_plan_url: not found
                il.add_xpath('store_image_url',
                            '../../div[@class="column last"]/img/@src',
                            TakeFirst())
                il.add_xpath('store_name', 'div[@class="store-name"]/text()',
                            TakeFirst(), unicode.strip)
                il.add_xpath('store_id', '/html/head/meta[@name="omni_page"]/@content',
                            TakeFirst(), re=r'(R\d+)$')
                # find weekly_ad_url: on the same page
                il.add_value('weekly_ad_url', response.url)
                il.add_value('store_url', response.url)
                il.add_xpath('zipcode', './/span[@class="postal-code"]/text()',
                            TakeFirst())

                yield il.load_item()

        
        next_page = response.css('div.pagination')
        next_page = next_page.css('a::attr(href)')[-1].get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)