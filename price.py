#-*- coding:utf8-*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import re
import time
from datetime import datetime
from urllib import quote
from selenium import webdriver
from pyquery import PyQuery as pq
from threading import Thread


class IConsole:
    """tool for console"""
    @staticmethod
    def now():
        return datetime.now().strftime("%Y-%M-%d %H:%M:%S")

    @staticmethod
    def log(self, msg):
        with open('browser.log', 'wt') as f:
            f.write(IConsole.now() + "  "+msg)
            f.write('\n')


class IBrowser(object):
    """a browser to run javascript"""
    browser = None

    def __init__(self):
        super(IBrowser, self).__init__()
        self.browser = webdriver.PhantomJS()

    def check_browser(self):
        if self.browser is not None:
            pass
        else:
            return {'errorMsg': 'web引擎异常'}

    def get(self, url):
        self.check_browser()
        try:
            print url
            self.browser.implicitly_wait(10)
            self.browser.get(url)
            return self.browser.page_source
        except Exception as e:
            print e
            msg = {'errorMsg': '网络异常'}
            IConsole.log(self, msg['errorMsg'])
            return msg


class Pricer(object):
    """docstring for Price
    DESCRITION: Check the price from Tmall.com  JD.com and suning.com
    INIT: good_name
    """
    good_name = None
    base_urls = ['https://list.tmall.com/search_product.htm?&sort=rq&',
        'http://search.jd.com/Search?&psort=3&']
    encoded_urls = {'tmall':'', 'jd':''}
    price = {'tmall': 0.0, 'jd': 0.0}
    link = {'tmall':'', 'jd':''}
    title = {'tmall':'', 'jd':''}

    def __init__(self, good_name):
        super(Pricer, self).__init__()
        self.good_name = good_name

    def check_property(self):
        if self.good_name is not None and\
         self.good_name is not '':
            pass
        else:
            return {'errorMsg': '不合法的查询参数'}

    def urlencoder(self):
        self.check_property()
        self.encoded_urls['tmall'] = self.base_urls[0] + 'q=' + self.good_name
        self.encoded_urls['jd'] = self.base_urls[1]+"keyword="+self.good_name+"&enc=utf-8"

    def jd_price(self):
        page_jd = IBrowser().get(self.encoded_urls['jd'])
        doc_jd = pq(page_jd)
        self.link['jd'] = 'http:' + pq(doc_jd('.p-img a')[0]).attr('href')
        self.price['jd'] = pq(doc_jd('.p-price i')[0]).text()
        self.title['jd'] = pq(doc_jd('.p-name em')[0]).text()

    def tmall_price(self):
        page_tmall = IBrowser().get(self.encoded_urls['tmall'])
        doc_tmall = pq(page_tmall)
        self.link['tmall'] = 'http:' + pq(doc_tmall('.productImg-wrap a')[0]).attr('href')
        self.price['tmall'] = pq(doc_tmall('.productPrice em')[0]).attr('title')
        self.title['tmall'] = pq(doc_tmall('.productTitle')[0]).text()

    def price_run(self):
        self.urlencoder()
        tt = Thread(target=self.tmall_price, args=())
        tj = Thread(target=self.jd_price, args=())
        tt.start()
        tj.start()
        while tt.isAlive() or tj.isAlive():
            time.sleep(0.1)

    def response(self):
        result = {'price': self.price, 'title': self.title, 'link': self.link}
        return result
