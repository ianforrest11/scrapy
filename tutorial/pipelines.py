import psycopg2
from scrapy.exceptions import DropItem
import json


class JobPipeline(object):
    def __init__(self):
        self.create_connection()
        self.create_table()
    
    # look up test indexing
    def create_connection(self):
        self.conn = psycopg2.connect(dbname = 'ceforqty', user= "ceforqty", password="GYh0O6sCjsdPPgZXg4DRYzL3Y9LDC5gl", host="salt.db.elephantsql.com")
        self.cursor = self.conn.cursor()
        
    def create_table(self):
        self.cursor.execute("""DROP TABLE IF EXISTS jobs_tb""")
        self.cursor.execute("""create table jobs_tb(
                  job_id text,
                  job_position text,
                  company_name text,
                  job_location text,
                  job_salary text,
                  job_description text,
                  published_at text,
                  application_link text,
                  source text
                  )""")
    
    def process_item(self, item, spider):
        self.store_db(item)
        return item
    
    def store_db(self, item):
        self.cursor.execute("""INSERT INTO jobs_tb VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",(
            item['job_id'],
            item['job_position'],
            item['company_name'],
            item['job_location'],
            item['job_salary'],
            item['job_description'],
            item['published_at'],
            item['application_link'],
            item['source']
        ))
        self.conn.commit()


class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['job_id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['job_id'])
            return item


class BlankPipeline(object):

    def process_item(self, item, spider):
        if item.get('job_salary'):
            item['job_salary'] = item['job_salary']
            return item
        else:
            item['job_salary'] = 'Not Available'
            return item
        
        if item.get('company_name'):
            item['company_name'] = item['company_name']
            return item
        else:
            item['company_name'] = 'Not Available'
            return item


class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('jobs.json', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), default=str) + "\n"
        self.file.write(line)
        return item





