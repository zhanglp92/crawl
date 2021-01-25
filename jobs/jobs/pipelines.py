# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import pymysql

# useful for handling different item types with a single interface
from jobs.items import JobItem, Company


class JobsPipeline:
    def __init__(self):
        self.job_cols = ','.join([
            'channel_type', 'channel_company_url', 'company', 'job_name', 'job_salary', 'job_tags', 'job_addr'
        ])

        self.company_cols = ','.join([
            'channel_type', 'channel_company_url',
            'company', 'company_name',
            'company_url',
            'company_city',
            'company_scale',
            'company_scale_min',
            'company_scale_max',
            'company_person',
            'company_phone',
            'company_email',
            'company_job_num',
        ])

    # 打开数据库
    def open_spider(self, spider):
        db = spider.settings.get('MYSQL_DB_NAME', 'jobs')
        host = spider.settings.get('MYSQL_HOST', '127.0.0.1')
        port = spider.settings.get('MYSQL_PORT', 3306)
        user = spider.settings.get('MYSQL_USER')
        passwd = spider.settings.get('MYSQL_PASSWORD')

        self.db_conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset='utf8')
        spider.logger.info('connect mysql successfully.')

    # 关闭数据库
    def close_spider(self, spider):
        self.db_conn.commit()
        self.db_conn.close()
        spider.logger.info('close mysql successfully.')

    def process_item(self, item, spider):
        if type(item) is JobItem:
            self.job_insert_db(item, spider)
        elif type(item) is Company:
            self.company_insert_db(item, spider)

        return item

    # 插入数据
    def company_insert_db(self, item, spider):
        db_cur = self.db_conn.cursor()

        sql = 'SELECT count(*) FROM company WHERE channel_type=%s AND company=%s'
        db_cur.execute(sql, (item['channel_type'], item['company']))
        num = db_cur.fetchall()[0][0]
        if num > 0:
            return

        values = (
            item['channel_type'],
            item['channel_company_url'],
            item['company'],
            item['company_name'],
            item['company_url'],
            item['company_city'],
            item['company_scale'],
            item['company_scale_min'],
            item['company_scale_max'],
            item['company_person'],
            item['company_phone'],
            item['company_email'],
            item['company_job_num'],
        )

        sql = 'INSERT INTO company (' + self.company_cols + ') VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        db_cur.execute(sql, values)
        spider.logger.info(f'insert {values}'.format(values=values))
        self.db_conn.commit()

    # 插入数据
    def job_insert_db(self, item, spider):
        db_cur = self.db_conn.cursor()

        sql = 'SELECT count(*) FROM job WHERE channel_type=%s AND company=%s AND job_name=%s'
        db_cur.execute(sql, (item['channel_type'], item['company'], item['job_name']))
        num = db_cur.fetchall()[0][0]
        if num > 0:
            return

        values = (
            item['channel_type'],
            item['channel_company_url'],
            item['company'],
            item['job_name'],
            item['job_salary'],
            item['job_tags'],
            item['job_addr'],
        )

        sql = 'INSERT INTO job (' + self.job_cols + ') VALUES(%s,%s,%s,%s,%s,%s,%s)'
        db_cur.execute(sql, values)
        spider.logger.info(f'insert {values}'.format(values=values))
        self.db_conn.commit()
