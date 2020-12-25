import scrapy
from scrapy import Request
from scrapy.http import Response
from scrapy.loader import ItemLoader
import json
from scrapy_selenium import SeleniumRequest
from selenium.common.exceptions import NoSuchElementException, NoSuchFrameException
from selenium.webdriver import Chrome, ActionChains
from selenium.webdriver.support import expected_conditions as EC  # 显性等待
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import requests
import random
import cv2 as cv
import numpy as np
from ..items import MovieCommentItem


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
        for account in self.accounts:
            yield SeleniumRequest(url='https://www.douban.com/', wait_time=10, callback=self.login,
                                  meta={'name': account['name'], 'password': account['password']})

    @staticmethod
    def save_img(bk_block):
        """保存图片"""
        try:
            img = requests.get(bk_block).content
            with open('bg.jpeg', 'wb') as f:
                f.write(img)
            return True
        except:
            return False

    @staticmethod
    def get_pos():
        """识别缺口
        注意：网页上显示的图片为缩放图片，缩放 50% 所以识别坐标需要 0.5
        """
        image = cv.imread('bg.jpeg')
        blurred = cv.GaussianBlur(image, (5, 5), 0)
        canny = cv.Canny(blurred, 200, 400)
        contours, hierarchy = cv.findContours(canny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        for i, contour in enumerate(contours):
            m = cv.moments(contour)
            if m['m00'] == 0:
                cx = cy = 0
            else:
                cx, cy = m['m10'] / m['m00'], m['m01'] / m['m00']
            if 6000 < cv.contourArea(contour) < 8000 and 370 < cv.arcLength(contour, True) < 390:
                if cx < 400:
                    continue
                x, y, w, h = cv.boundingRect(contour)  # 外接矩形
                cv.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                # cv.imshow('image', image)  # 显示识别结果
                print(f'【缺口识别】 {x / 2} px')
                return x / 2
        return 0

    @staticmethod
    def get_track(distance):
        """模拟轨迹
        """
        distance -= 68  # 初始位置
        # 初速度
        v = 0
        # 单位时间为0.2s来统计轨迹，轨迹即0.2内的位移
        t = 0.2
        # 位移/轨迹列表，列表内的一个元素代表0.2s的位移
        tracks = []
        # 当前的位移
        current = 0
        # 到达mid值开始减速
        mid = distance * 7 / 8

        distance += 10  # 先滑过一点，最后再反着滑动回来
        # a = random.randint(1,3)
        while current < distance:
            if current < mid:
                # 加速度越小，单位时间的位移越小,模拟的轨迹就越多越详细
                a = random.randint(1, 2)  # 加速运动
            else:
                a = -random.randint(1, 3)  # 减速运动

            # 初速度
            v0 = v
            # 0.2秒时间内的位移
            s = v0 * t + 0.5 * a * (t ** 2)
            # 当前的位置
            current += s
            # 添加到轨迹列表
            tracks.append(round(s))

            # 速度已经达到v,该速度作为下次的初速度
            v = v0 + a * t

        # 反着滑动到大概准确位置
        for i in range(4):
            tracks.append(-random.randint(2, 3))
        for i in range(4):
            tracks.append(-random.randint(1, 3))
        return tracks

    @staticmethod
    def ease_out_quart(x):
        return 1 - pow(1 - x, 4)

    @staticmethod
    def get_tracks_2(distance, seconds, ease_func):
        """
        根据轨迹离散分布生成的数学 生成  # 参考文档  https://www.jianshu.com/p/3f968958af5a
        成功率很高 90% 往上
        :param distance: 缺口位置
        :param seconds:  时间
        :param ease_func: 生成函数
        :return: 轨迹数组
        """
        distance -= 68  # 初始位置
        distance += 20
        tracks = [0]
        offsets = [0]
        for t in np.arange(0.0, seconds, 0.1):
            ease = ease_func
            offset = round(ease(t / seconds) * distance)
            tracks.append(offset - offsets[-1])
            offsets.append(offset)
        tracks.extend([-3, -2, -3, -2, -2, -2, -2, -1, -0, -1, -1, -1])
        return tracks

    def login(self, response):
        browser: Chrome = response.request.meta['driver']
        browser.delete_all_cookies()
        time.sleep(0.5)
        browser.switch_to.frame(0)
        browser.find_element_by_xpath('/html/body/div[1]/div[1]/ul[1]/li[2]').click()
        browser.find_element_by_xpath('//*[@id="username"]').send_keys(response.request.meta['name'])
        browser.find_element_by_xpath('//*[@id="password"]').send_keys(response.request.meta['password'])
        browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[5]/a').click()
        time.sleep(2)
        cookie = browser.get_cookie('dbcl2')
        if not cookie:
            try:
                WebDriverWait(browser, 10, 0.5).until(
                    EC.presence_of_element_located((By.ID, 'tcaptcha_iframe')))  # 等待 iframe
                browser.switch_to.frame(browser.find_element_by_id('tcaptcha_iframe'))  # 加载 iframe
                time.sleep(0.5)
            except NoSuchFrameException:
                print('No reCAPTCHA NoSuchFrameException')
            except NoSuchElementException:
                print('No reCAPTCHA NoSuchElementException')
            else:
                bk_block = browser.find_element_by_xpath('//*[@id="slideBg"]').get_attribute('src')
                if self.save_img(bk_block):
                    dex = self.get_pos()
                    # track_list = self.get_track(dex)
                    track_list = self.get_tracks_2(dex, 3, self.ease_out_quart)
                    time.sleep(0.52)
                    slid_ing = browser.find_element_by_xpath('//div[@id="tcaptcha_drag_thumb"]')  # 滑块定位
                    ActionChains(browser).click_and_hold(on_element=slid_ing).perform()  # 鼠标按下
                    time.sleep(0.21)
                    print('轨迹', track_list)
                    for track in track_list:
                        ActionChains(browser).move_by_offset(xoffset=track, yoffset=0).perform()  # 鼠标移动到距离当前位置（x,y）
                    time.sleep(0.441)
                    ActionChains(browser).release(on_element=slid_ing).perform()  # print('第三步,释放鼠标')
                    # 识别图片
                    time.sleep(2)
                    cookie = browser.get_cookie('dbcl2')
                else:
                    print('缺口图片捕获失败')
        browser.quit()
        if cookie:
            self.cookies.append({'dbcl2': eval(cookie['value'])})
            if len(self.cookies) >= len(self.accounts) / 2:
                print('登录完成，开始爬取...')
                yield Request(url=self.base_url,
                              meta={'cookiejar': 1, 'dont_redirect': True, 'handle_httpstatus_list': [302]},
                              callback=self.parse, dont_filter=True)
        else:
            print(f'用户 {response.request.meta["name"]} 登录失败')
            return None

    def parse(self, response, **kwargs):
        for comment in response.css('div.comment-item'):
            item = MovieCommentItem()
            item['name'] = comment.xpath('div[2]/h3/span[2]/a/text()').get()
            item['seen'] = comment.xpath('div[2]/h3/span[2]/span[1]/text()').get()
            item['star'] = comment.xpath('div[2]/h3/span[2]/span[has-class("rating")]/@title').get()
            item['date'] = comment.xpath('div[2]/h3/span[2]/span[has-class("comment-time")]/@title').get()
            item['votes'] = comment.xpath('div[2]/h3/span[1]/span/text()').get()
            item['text'] = comment.xpath('div[2]/p/span/text()').get()
            yield item
        next_page = response.css('a.next::attr("href")')
        if next_page.get() is not None:
            start = next_page.re_first(r'\?start=(\d+)')
            if self.end == -1 or self.end > int(start) / 20:
                yield response.follow(next_page.get(), self.parse, dont_filter=True)
