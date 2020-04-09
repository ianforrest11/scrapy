import scrapy
from scrapy.crawler import CrawlerProcess
from .indeed_spider import IndeedSpider
from .weworkremotely_spider import WeWorkRemotelySpider

# execute with 'scrapy crawl [filename]', in this case 'crawler'
process = CrawlerProcess()
process.crawl(IndeedSpider)
process.crawl(WeWorkRemotelySpider)
process.start()
