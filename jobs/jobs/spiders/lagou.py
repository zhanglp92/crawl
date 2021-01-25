# -*- coding:utf-8 -*-
# import sys
# sys.path.append(r'../../')
import scrapy

from jobs.items import JobItem


class LagouSpider(scrapy.Spider):
    login = False
    name = 'lagou'
    allowed_domains = ['lagou.com']

    def __build_lg_url(self, ty, page):
        return 'https://www.lagou.com/zhaopin/{ty}/{page}/'.format(ty=ty, page=page)

    def start_requests(self):
        cates = {
            'C++youxikaifa': 30,
            'COCOS2D-X1': 30,
            'H5youxikaifa': 30,
            'U3D': 30,
            'dianjingjiangshi': 30,
            'juqingsheji': 30,
            'shouyoutuiguang': 30,
            'youxibianji': 30,
            'youxichangjing1': 30,
            'youxiflash': 30,
            'youxihouduankaifa': 30,
            'youximeigong': 30,
            'youxiyunying': 30,
            'youxijiemian': 29,
            'dianjingzhuchi': 28,
            'youxituiguang': 28,
            'xiaoyouxikaifa': 27,
            'youxicehua': 26,
            'youxiyouxiceshi': 26,
            'youxizhipianren': 26,
            'youxipeilian': 24,
            'youxixiangmujingli': 21,
            'youxiU3D': 18,
            'youxidongxiao': 16,
            'youxidongzuo1': 15,
            'youxichanpinjingli': 14,
            'youxidonghua': 14,
            'youxijuese': 14,
            'youxitiyan': 13,
            'youxiwenan': 12,
            'youxiyouxicehua': 12,
            'youxiyuanhua': 12,
            'youxiyunying1': 11,
            'youxizhuobo': 11,
            'yeyoutuiguang': 9,
        }

        for ty, page in cates.items():
            yield scrapy.Request(self.__build_lg_url(ty, page + 1))

    def parse(self, response, **kwargs):
        job_list = response.xpath("//div[@id='s_position_list']/ul/li")
        for i in job_list:
            p_top = i.xpath(".//div[@class='list_item_top']/div[@class='position']/div[@class='p_top']")[0]
            company = i.xpath(".//div[@class='company']/div[@class='company_name']")[0]

            item = JobItem(
                channel_type='lagou',
                channel_company_url=company.xpath(".//a/@href")[0].get(),
                job_name=i.xpath(".//@data-positionname")[0].get(),
                job_salary=i.xpath(".//@data-salary")[0].get(),
                job_tags='/'.join(i.xpath(".//div[@class='list_item_bot']/div[@class='li_b_l']/span/text()").getall()),
                job_addr=p_top.xpath(".//a/span/em/text()")[0].get(),
                company=i.xpath(".//@data-company")[0].get(),
            )
            yield item

        next_page = response.xpath("//div[@class='item_con_pager']/div[@class='pager_container']/a/@href")

        if len(next_page) > 0:
            yield scrapy.Request(next_page[-1].get())


if __name__ == '__main__':
    from lxml import etree  # path = './web/new_index.html'

    fp = open('lagou.html', 'rb')
    html = fp.read().decode('utf-8')  # .decode('gbk')
    rr = etree.HTML(html)  # etree.HTML(源码) 识别为可被xpath解析的对象

    for job in LagouSpider(scrapy.Spider(name='test')).parse(response=rr):
        print(job)
