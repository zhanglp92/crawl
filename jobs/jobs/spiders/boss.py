# -*- coding:utf-8 -*-

import scrapy

from jobs.items import JobItem


class BossSpider(scrapy.Spider):
    name = 'boss'
    allowed_domains = ['zhipin.com']
    start_urls = ['https://www.zhipin.com/job_detail/?query=游戏&city=100010000']
    base_url = 'https://www.zhipin.com'

    def parse(self, response, **kwargs):
        job = response.xpath("//div[@class='job-list']/ul/li")
        for i in job:
            item = JobItem(
                channel_type='boss',
                channel_company_url='https://www.zhipin.com/' + i.xpath(".//h3[@class='name']/a/@href").get(),
                job_name=i.xpath(".//span[@class='job-name']/a/text()").get(),
                job_salary=i.xpath(".//span[@class='red']/text()").get(),
                job_tags='/'.join(i.xpath(".//div[@class='tags']/span/text()").getall()),
                job_addr=i.xpath(".//span[@class='job-area-wrapper']/span/text()").get(),
                company=i.xpath(".//h3[@class='name']/a/text()").get(),
            )
            yield item

        # 获取下一页的地址
        page = response.xpath("//div[@class='page']/a[last()]/@href").get()
        next_url = self.base_url + page
        if not next_url:
            self.logger.info('exit')
            return
        else:
            self.logger.info('next page {url}'.format(url=next_url))
            yield scrapy.Request(next_url)
