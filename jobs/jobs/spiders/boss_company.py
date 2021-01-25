# -*- coding:utf-8 -*-

# import sys
#
# sys.path.append(r'../../')

import pymysql
import scrapy

from jobs.items import Company
from jobs.spiders.util import CompanyScale


class BossCompanySpider(scrapy.Spider):
    name = 'boss_company'
    allowed_domains = ['zhipin.com']

    def start_requests(self):
        urls = GetCompanyURL().get_url(self)
        for u in urls:
            yield scrapy.Request(u)

    def parse(self, response, **kwargs):
        home_inner = response.xpath("//div[@class='company-banner']/div[@class='inner home-inner']/div/div")
        print('------>', home_inner)

        state, primary = home_inner[0], home_inner[1]

        business = response.xpath("//div[@class='job-sec company-business']")[0]
        business_info = business.xpath(".//div[@class='business-detail']/ul/li")
        company_scale = primary.xpath(".//div/p/text()")[1].strip()
        scale_min, scale_max = CompanyScale(company_scale)

        item = Company(
            channel_type='boss',
            channel_company_url='https://www.zhipin.com' + state.xpath(".//span/a/@href")[0],
            company_job_num=state.xpath(".//span/a[@ka='all-jobs-top']/b/text()")[0],
            company=primary.xpath(".//div/h1/text()")[0],
            company_scale=company_scale,
            company_scale_min=scale_min,
            company_scale_max=scale_max,
            company_name=business.xpath(".//h4/text()")[0],
            company_person=business_info[0].xpath(".//text()")[1],
            company_city=business_info[5].xpath(".//text()")[1],
        )
        yield item


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
            sql = 'SELECT DISTINCT channel_company_url FROM job WHERE channel_type = %s'
            self.db_cur.execute(sql, 'boss')
            # urls = []
            for record in self.db_cur.fetchall():
                yield record[0]
        finally:
            self.__close(spider)


if __name__ == '__main__':
    from lxml import etree  # path = './web/new_index.html'

    fp = open('boss_company.html', 'rb')
    html = fp.read().decode('utf-8')  # .decode('gbk')
    rr = etree.HTML(html)  # etree.HTML(源码) 识别为可被xpath解析的对象

    for node in BossCompanySpider(scrapy.Spider(name='test')).parse(response=rr):
        print(node)
