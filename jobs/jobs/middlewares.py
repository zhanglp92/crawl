# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import base64
import random

from scrapy import signals
from scrapy.http.response.html import HtmlResponse
from selenium import webdriver

from jobs.settings import PROXIES, USER_AGENTS


# useful for handling different item types with a single interface


class JobsSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class JobsDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class CookiesMiddlewares(object):
    def __init__(self):
        self.driver = webdriver.Chrome()

    def process_request(self, request, spider):
        spider.logger.info('simulate chrome get {url}'.format(url=request.url))
        self.driver.get(request.url)
        # time.sleep(random.randint(2, 3))  # 我们等待5秒钟，让其加载
        input("人工触发:")
        source = self.driver.page_source
        response = HtmlResponse(url=self.driver.current_url, body=source, request=request, encoding='utf-8')
        return response


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        proxy = random.choice(PROXIES)
        if proxy['user_pass'] is not None:
            request.meta['proxy'] = "http://%s" % proxy['ip_port']
            encoded_user_pass = base64.b64encode(proxy['user_pass'].encode('utf-8'))
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass.decode()
            request.headers[
                'cookie'] = 'user_trace_token=20210123161121-890cbfee-c38f-4e7a-a7c4-a65dda5b538e; __lg_stoken__=a5f4c8d5a548a0ce6b982aab6ebc831ce38181343fb2b6b4de6bb55ecc76c50de1e99915829b4f3f4650cff020b1d35af543169b07fad2facfb5ed14291b1eb070b5d01fc3a6; JSESSIONID=ABAAAECABFAACEAFE77C5A5EEF550278CF2518DC5F8DCEE; WEBTJ-ID=20210123161122-1772e4c376d695-020474c96b7cbb-326e7006-2073600-1772e4c376e104b; sajssdk_2015_cross_new_user=1; sensorsdata2015session=%7B%7D; PRE_UTM=; PRE_HOST=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fzhaopin%2FH5youxikaifa%2F1%2F; LGSID=20210123161123-0b279496-5fbe-4ceb-8ef0-f61507b66da9; PRE_SITE=; LGUID=20210123161123-f31f6be1-749a-4601-bb80-98245d8007fa; _ga=GA1.2.442127149.1611389483; _gid=GA1.2.1104372499.1611389483; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1611389483; SEARCH_ID=c21bc77202e040f4bb186683c4f59d47; sm_auth_id=wwjj436j8wg7fout; gate_login_token=d94d3f2415ab9b4593db716e65a0c13fd1403163ea46e662; RECOMMEND_TIP=true; _putrc=DEC2E05A3BA2378E; _gat=1; login=true; unick=%E5%BC%A0%E5%88%A9%E9%B9%8F; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=53; privacyPolicyPopup=false; index_location_city=%E5%85%A8%E5%9B%BD; X_HTTP_TOKEN=2a24b18ad5cd61931510931161bfab1168157d1fdc; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%224028121%22%2C%22first_id%22%3A%221772e4c387c22c-0ab8501087025f-326e7006-2073600-1772e4c387d1066%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24os%22%3A%22MacOS%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%2287.0.4280.141%22%2C%22lagou_company_id%22%3A%22%22%7D%2C%22%24device_id%22%3A%221772e4c387c22c-0ab8501087025f-326e7006-2073600-1772e4c387d1066%22%7D; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1611390152; LGRID=20210123162232-5d333ecf-2733-44a3-8758-796aa58a208a; TG-TRACK-CODE=index_navigation'

            print("**************ProxyMiddleware have pass************" + proxy['ip_port'])
        else:
            print("**************ProxyMiddleware no pass************" + proxy['ip_port'])
            request.meta['proxy'] = "http://%s" % proxy['ip_port']


class RandomUserAgent(object):
    """Randomly rotate user agents based on a list of predefined ones"""

    def process_request(self, request, spider):
        # print('---------------> self.agents={agents}'.format(agents=USER_AGENTS))
        request.headers.setdefault('User-Agent', random.choice(USER_AGENTS))
