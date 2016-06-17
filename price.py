#-*- coding:utf8-*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import re

from datetime import datetime
from urllib import quote
from selenium import webdriver


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
    page_source = None

    def __init__(self):
        super(IBrowser, self).__init__()
        self.browser = webdriver.PhantomJS()

    def check_browser(self, requst_method):
        if self.browser is not None:
            requst_method()
        else:
            return {'errorMsg': 'web引擎异常'}

    #@check_browser
    def get(self, url):
        try:
            print url
            self.browser.implicitly_wait(3)
            self.browser.get(url)
            f = open('huawei.html', 'w')
            f.write(self.browser.page_source)
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
    base_urls = ['https://list.tmall.com/search_product.htm?&sort=s&',
        'http://search.jd.com/Search?',
        'http://search.suning.com/']
    encoded_urls = {'tmall':'', 'jd':'','suning':''}
    price = {'tmall': 0.0, 'jd': 0.0, 'suning': 0.0}

    def __init__(self, good_name):
        super(Pricer, self).__init__()
        self.good_name = good_name

    def check_property(self, func):
        if self.good_name is not None and\
         self.good_name is not '':
            sort()
        else:
            return {'errorMsg': '不合法的查询参数'}

    #@check_property
    def urlencoder(self):
        self.encoded_urls['tmall'] = self.base_urls[0] + 'q=' + quote(self.good_name)
        self.encoded_urls['jd'] = self.base_urls[1]+"keyword="+self.good_name+"&enc=utf-8"
        self.encoded_urls['suning'] = self.base_urls[2]+self.good_name+'/'

    def get_price(self):
        self.urlencoder()
        page_tmall = IBrowser().get(self.encoded_urls['tmall'])
        pattern_tmall = re.compile(r'id="J_ItemList.*?href="(.*?)".*?em title="(.*?)".*?_blank" title="(.*?)"', re.S)
        result_tmall = re.findall(pattern_tmall, page_tmall)
        for item in result_tmall:
            print item[0]
            print item[1]
            print item[2]
        #page_jd = IBrowser.get(self.encoded_urls['tmall'])
        #page_suning = IBrowser.get(self.encoded_urls['tmall'])


pricer = Pricer("华为p8")
pricer.get_price()
