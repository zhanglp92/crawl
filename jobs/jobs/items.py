# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobItem(scrapy.Item):
    # 渠道相关
    channel_type = scrapy.Field()  # 渠道类型
    channel_company_url = scrapy.Field()  # 渠道公司简介

    company = scrapy.Field()  # 公司名

    # 职位相关
    job_name = scrapy.Field()  # 职位名称
    job_salary = scrapy.Field()  # 薪资
    job_tags = scrapy.Field()  # tags
    job_addr = scrapy.Field()  # 公司地址


class Company(scrapy.Item):
    # 渠道相关
    channel_type = scrapy.Field()  # 渠道类型
    channel_company_url = scrapy.Field()  # 渠道公司简介

    # 公司相关
    company = scrapy.Field()  # 公司名
    company_name = scrapy.Field()  # 公司名全称
    company_url = scrapy.Field()  # 公司官网
    company_city = scrapy.Field()  # 城市
    company_scale = scrapy.Field()  # 规模
    company_scale_min = scrapy.Field()  # 规模
    company_scale_max = scrapy.Field()  # 规模
    company_person = scrapy.Field()  # 法人
    company_phone = scrapy.Field()  # 电话
    company_email = scrapy.Field()  # 邮箱
    company_job_num = scrapy.Field()  # 职位数量
