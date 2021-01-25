# -*- coding:utf-8 -*-
import json
import re

import pymysql
import scrapy

from jobs.items import Company
from jobs.spiders.util import CompanyScale


class LagouCompanySpider(scrapy.Spider):
    login = False
    name = 'lagou_company'
    allowed_domains = ['lagou.com']

    def start_requests(self):
        urls = GetCompanyURL().get_url(self)
        for u in urls:
            yield scrapy.Request(u)

    def parse(self, response, **kwargs):
        company_data = response.xpath("//div[@class='company_data']/ul/li/strong/text()").get()
        if company_data is None:
            return None

        company_job_num = 0
        if company_data is not None:
            group = re.match(r'(\d+)个', company_data.strip(), re.M | re.I)
            company_job_num = int(group.group(1))

        company_data = response.xpath("//script[@id='companyInfoData']/text()").get()
        # print('------companyInfoData->', response.xpath("//script[@id='companyInfoData']/text()").get())
        if company_data is None:
            return None
        company_data = company_data.replace('\n', '')
        company_data = json.loads(company_data)

        if company_data is None:
            return None

        company_scale_min, company_scale_max = CompanyScale(company_data['baseInfo']['companySize'])

        company_person = ''
        if 'leaders' in company_data and len(company_data['leaders']) > 0 and 'name' in company_data['leaders'][0]:
            company_person = company_data['leaders'][0]['name']

        company_item = Company(
            channel_type='lagou',
            channel_company_url=company_data['coreInfo']['companyUrl'],
            company=company_data['coreInfo']['companyShortName'],
            company_name=company_data['coreInfo']['companyName'],
            company_url='',
            company_city=company_data['baseInfo']['city'],
            company_scale=company_data['baseInfo']['companySize'],
            company_scale_min=company_scale_min,
            company_scale_max=company_scale_max,
            company_person=company_person,
            company_phone='',
            company_email='',
            company_job_num=company_job_num,
        )

        yield company_item


class GetCompanyURL(object):
    def __conn(self, spider):
        db = spider.settings.get('MYSQL_DB_NAME', 'jobs')
        host = spider.settings.get('MYSQL_HOST', '127.0.0.1')
        port = spider.settings.get('MYSQL_PORT', 3306)
        user = spider.settings.get('MYSQL_USER')
        passwd = spider.settings.get('MYSQL_PASSWORD')

        self.db_conn = pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset='utf8')
        self.db_cur = self.db_conn.cursor()
        spider.logger.info('connect mysql successfully.')

    # 关闭数据库
    def __close(self, spider):
        self.db_conn.commit()
        self.db_conn.close()
        spider.logger.info('close mysql successfully.')

    # 插入数据
    def get_url(self, spider):
        self.__conn(spider)
        try:
            sql = 'SELECT MAX(channel_company_url) FROM job WHERE channel_type = %s GROUP BY company LIMIT 1650, 3000'
            self.db_cur.execute(sql, 'lagou')
            # urls = []
            for record in self.db_cur.fetchall():
                yield record[0]
                # spider.logger.info('----> company url: {res}'.format(res=u))
                # urls.append(u)
            # return urls
        finally:
            self.__close(spider)


if __name__ == '__main__':
    from lxml import etree  # path = './web/new_index.html'

    fp = open('lagou.html', 'rb')
    html = fp.read().decode('utf-8')  # .decode('gbk')
    rr = etree.HTML(html)  # etree.HTML(源码) 识别为可被xpath解析的对象

    for job in LagouCompanySpider(scrapy.Spider(name='test')).parse(response=rr):
        print(job)
