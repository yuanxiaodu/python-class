import scrapy
from scrapy import Request
from scrapy.http import Response
import json


# scrapy crawl movie_comment -o movie_comments.csv -a id=27073752 -a start=1 -a end=1 -a sort=new_score
class MovieCommentSpider(scrapy.Spider):
    name = "movie_comment"
    allowed_domains = ['douban.com']
    # 建立cookie池
    cookies = []

    def __init__(self, start=1, end=1, sort='new_score', **kwargs):
        """
        :param start: 起始页（包含）
        :param end: 结束页（包含）
        :param sort: # 'new_score'（热门） or 'time'（最新）
        :param kwargs:
        """
        self.end = int(end)
        self.base_url = f'https://movie.douban.com/subject/{kwargs["id"]}/comments?start={(int(start) - 1) * 20}&limit=20&status=P&sort={sort}'
        with open('../../douban_accounts.json', encoding='UTF-8') as f:
            js = json.load(f)
            self.accounts = js['accounts']
        super().__init__(**kwargs)

    def start_requests(self):
        return [Request(url='https://www.douban.com/', meta={'cookiejar': 1}, callback=self.login)]

    def login(self, response):
        for account in self.accounts:
            # 在循环中使用douban_accounts.json中那几个账号登录,dont_filter参数用来防止不同的请求被过滤掉，URL去重默认是打开的
            yield scrapy.FormRequest(
                url='https://accounts.douban.com/j/mobile/login/basic',
                method='POST',
                formdata={
                    'ck': '',
                    'remember': 'false',
                    'name': account['name'],
                    'password': account['password']
                },
                meta={'cookiejar': response.meta['cookiejar']},
                dont_filter=True,
                callback=self.add_cookie
            )

    def add_cookie(self, response: Response):
        # 将cookie保存起来
        if json.loads(response.text)['status'] != 'success':
            print(f'login failed, message: {response.text}')
            return None
        cookiejar = response.headers.get('Set-Cookie').decode()
        cookie = dict([cookiejar.split('; ')[0].split('=')])
        cookie['dbcl2'] = eval(cookie['dbcl2'])
        self.cookies.append(cookie)
        # 当全部账号都已经登录成功后即可开始爬取流程
        if len(self.cookies) >= len(self.accounts):
            print('登录完成，开始爬取...')
            yield Request(url=self.base_url,
                          meta={'cookiejar': 1, 'dont_redirect': True, 'handle_httpstatus_list': [302]},
                          callback=self.parse, dont_filter=True)

    def parse(self, response, **kwargs):
        for comment in response.css('div.comment-item'):
            yield {
                'name': comment.xpath('div[2]/h3/span[2]/a/text()').get(),
                'seen': comment.xpath('div[2]/h3/span[2]/span[1]/text()').get(),
                'star': comment.xpath('div[2]/h3/span[2]/span[has-class("rating")]/@title').get(),
                'date': comment.xpath('div[2]/h3/span[2]/span[has-class("comment-time")]/@title').get(),
                'votes': comment.xpath('div[2]/h3/span[1]/span/text()').get(),
                'text': comment.xpath('div[2]/p/span/text()').get()
            }
        next_page = response.css('a.next::attr("href")')
        if next_page.get() is not None:
            start = next_page.re_first(r'\?start=(\d+)')
            if self.end == -1 or self.end > int(start) / 20:
                yield response.follow(next_page.get(), self.parse, dont_filter=True)
