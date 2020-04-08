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
                  job_title text,
                  company text,
                  location text,
                  salary text,
                  rating text,
                  job_desc text,
                  date_posted text,
                  link text
                  )""")
    
    def process_item(self, item, spider):
        self.store_db(item)
        return item
    
    def store_db(self, item):
        self.cursor.execute("""INSERT INTO jobs_tb VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",(
            item['job_id'][0],
            item['job_title'][0],
            item['company'][0],
            item['location'][0],
            item['salary'][0],
            item['rating'][0],
            item['job_desc'][0],
            item['date_posted'][0],
            item['link']
        ))
        self.conn.commit()
