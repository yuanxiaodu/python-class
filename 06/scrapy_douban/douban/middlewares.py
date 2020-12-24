# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import requests
import random
from scrapy import signals


class DoubanSpiderMiddleware:
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


class DoubanDownloaderMiddleware:
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


class ProxyMiddleware(DoubanDownloaderMiddleware):
    def __init__(self):
        self.proxy_list = []
        self.update_proxy_list()
        super(ProxyMiddleware, self).__init__()

    def update_proxy_list(self):
        if len(self.proxy_list) < 100:
            r = requests.get(
                'http://webapi.http.zhimacangku.com/getip?num=200&type=1&pro=&city=0&yys=0&port=1&pack=131112&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=')
            if r.status_code == 200:
                self.proxy_list += r.text.splitlines()

    def process_request(self, request, spider):
        proxy = random.choice(self.proxy_list).strip()
        print("this is response ip: " + proxy)
        request.meta['proxy'] = f'http://{proxy}'

    def process_response(self, request, response, spider):
        if response.status != 200:
            print("this ip does not work: " + request.meta['proxy'])
            self.proxy_list.remove(request.meta['proxy'].split('//')[1])
            self.update_proxy_list()
            proxy = random.choice(self.proxy_list).strip()
            request.meta['proxy'] = f'http://{proxy}'
            return request
        return response


class CookieMiddleware(DoubanDownloaderMiddleware):
    def __init__(self):
        super(CookieMiddleware, self).__init__()

    def process_request(self, request, spider):
        if len(spider.cookies) >= len(spider.accounts):
            # 更换cookie
            request.cookies = random.choice(spider.cookies)
        # 为什么这里要返回None，不能返回request？返回request爬虫会直接关闭，无法接续爬，下篇文章中来解释，这里困扰了我半个晚上。
        return None

    def process_response(self, request, response, spider):
        # 如果遇到了403，更换cookie,和更换代理IP的思路是一样的
        if response.status == 403:
            print(f'cookie {request.cookies} 被ban，更换cookie')
            request.cookies = random.choice(spider.cookies)
            return request
        else:
            return response


if __name__ == '__main__':
    cookie = {
        # "bid": "U13XC3O9cuI",
        # "_ga": "GA1.2.983677805.1602411389",
        # "push_doumail_num": "0",
        # "_vwo_uuid_v2": "D9D7E6621CD8F1344A21BB0B0C14D5311|22e02d6a48b8c88990e99d25f333abfa",
        # "ll": "118371",
        # "gr_user_id": "44deef48-3f18-4369-889c-1fccea6f8d26",
        # "__gads": "ID=c6da4f22b0c4db23-22b84a3180c400cd:T=1604144661:RT=1604144661:S=ALNI_Ma6y8Kj8-LfsqHoH6jRAKsbgwr-ew",
        # "viewed": "30203158_26921709_35043941_30237842_27094555",
        # "push_noty_num": "0",
        # "_pk_ses.100001.8cb4": "*",
        # "__utmc": "30149280",
        # "__utmt": "1",
        "dbcl2": "48587960:bfE4PlaHacA",
        # "ck": "Io7c",
        # "ap_v": "0,6.0",
        # "__utmv": "30149280.4858",
        # "__utma": "30149280.983677805.1602411389.1608750512.1608750683.2",
        # "__utmz": "30149280.1608750683.2.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)",
        # "_pk_id.100001.8cb4": "82277fe1321e8001.1608750511.1.1608751062.1608750511.",
        # "__utmb": "30149280.19.9.1608751062505"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
    }
    session = requests.session()
    html = session.get("https://movie.douban.com/subject/27073752/comments?start=300&limit=20&status=P&sort=new_score",
                       headers=headers, cookies=cookie).text
    print('神奇女侠' in html)
