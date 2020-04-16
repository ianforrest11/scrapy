import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
import unicodedata


class JobItem(scrapy.Item):
    # define the fields for your item here like:
    job_id = scrapy.Field()
    job_position = scrapy.Field()
    company_name = scrapy.Field()
    job_location = scrapy.Field()
    job_salary = scrapy.Field()
    job_description = scrapy.Field()
    published_at = scrapy.Field()
    application_link = scrapy.Field()
    source = scrapy.Field()
    
class JobLoader(ItemLoader):
    default_item_class = JobItem
    default_output_processor = TakeFirst()
