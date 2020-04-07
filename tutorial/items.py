import scrapy


class JobItem(scrapy.Item):
    # define the fields for your item here like:
    job_id = scrapy.Field()
    job_title = scrapy.Field()
    company = scrapy.Field()
    location = scrapy.Field()
    salary = scrapy.Field()
    rating = scrapy.Field()
    job_desc = scrapy.Field()
    date_posted = scrapy.Field()
    link = scrapy.Field()