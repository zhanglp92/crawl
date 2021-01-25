# -*- coding:utf-8 -*-
import json

import scrapy

from jobs.items import JobItem, Company
from jobs.spiders.util import CompanyScale


class Q51JobSpider(scrapy.Spider):
    name = '51job'
    allowed_domains = ['51job.com']

    def __build_51url(self, page):
        return 'https://search.51job.com/list/000000,000000,0000,00,9,99,游戏,2,{page}.html'.format(page=page)

    def start_requests(self):
        yield scrapy.Request(self.__build_51url(1))

    def parse(self, response, **kwargs):
        context = response.xpath("//script[@type='text/javascript']/text()")[0].get()
        context = context.replace('window.__SEARCH_RESULT__ =', '')
        context_json = json.loads(context)
        # print(context_json['engine_search_result'])

        for node in context_json['engine_search_result']:
            job_item = JobItem(
                channel_type='51job',
                channel_company_url=node['company_href'],
                company=node['company_name'],
                job_name=node['job_name'],
                job_salary=node['providesalary_text'],
                job_addr=node['workarea_text'],
                job_tags='',
            )
            yield job_item

            scale_min, scale_max = CompanyScale(node['companysize_text'])
            company_item = Company(
                channel_type='51job',
                channel_company_url=node['company_href'],
                company_url='',
                company_person='',
                company_phone='',
                company_email='',
                company=node['company_name'],
                company_name=node['company_name'],
                company_city=node['workarea_text'],
                company_scale=node['companysize_text'],
                company_scale_min=scale_min,
                company_scale_max=scale_max,
                company_job_num=0,
            )
            yield company_item

        curr_page = int(context_json['curr_page'])
        total_page = int(context_json['total_page'])
        if curr_page < total_page:
            yield scrapy.Request(self.__build_51url(curr_page + 1))


if __name__ == '__main__':
    from lxml import etree  # path = './web/new_index.html'

    fp = open('51job.html', 'rb')
    html = fp.read().decode('gbk')
    rr = etree.HTML(html)  # etree.HTML(源码) 识别为可被xpath解析的对象

    for job in Q51JobSpider(scrapy.Spider(name='test')).parse(response=rr):
        print(job)
