from scrapy.crawler import CrawlerProcess
from tutorial.spiders.indeed_spider import IndeedSpider
from tutorial.spiders.monster_spider import MonsterSpider
from scrapy.utils.project import get_project_settings
from .items import JobItem, JobLoader

settings = get_project_settings()
process = CrawlerProcess(settings)
process.crawl(IndeedSpider)
process.crawl(MonsterSpider)
process.start()