# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2


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
            item['job_id'][0],
            item['job_position'][0],
            item['company_name'][0],
            item['job_location'][0],
            item['job_salary'][0],
            item['job_description'][0],
            item['published_at'][0],
            item['application_link'],
            item['source']
        ))
        self.conn.commit()
