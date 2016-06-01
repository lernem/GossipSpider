#! /usr/bin/env python
# coding:utf-8

import cookielib
import sys
import urllib
import urllib2
import bs4
import time
import Config

# Avoid Chinese encoding error.
reload(sys)
sys.setdefaultencoding("utf-8")


class SenderInfo:
    def __init__(self):
        self.sender = ''
        self.url = ''

# Sign in
login_url = 'http://3g.renren.com/login.do?autoLogin=true'
login_domain = '3g.renren.com'


class RenrenSpider(object):
    def __init__(self, username, pwd, domain, verify_key=''):
        self.username = username
        self.password = pwd
        self.domain = domain
        self.verify_key = verify_key

        self.cj = cookielib.LWPCookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        urllib2.install_opener(self.opener)

    def get_total_pages_count(self, gossip_page_url):
        gossip_page = urllib2.urlopen(gossip_page_url).read()
        soup = bs4.BeautifulSoup(gossip_page, 'lxml')
        for child in soup.find(class_="list").children:
            if child.p is None:  # Is the navigation line, get total count of pages here.
                tmp_lst = [text for text in child.strings]
                tmp_total_str = tmp_lst[5]  # Todo: Need consider about 1 page gossips
                total_str_start_idx = tmp_total_str.find('/') + 1
                total_str_end_idx = tmp_total_str.find('页')
                return int(tmp_total_str[total_str_start_idx:total_str_end_idx])
        return -1

    def login(self):
        """
        Login m.renren.com.
        :return: Prettified home page soup.
        """
        login_params = {'domain': self.domain, 'email': self.username, 'password': self.password}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'}
        req = urllib2.Request(login_url, urllib.urlencode(login_params), headers=headers)
        response = urllib2.urlopen(req)
        # home_page = response.read()
        return response.read()

    def get_user_id_from_user_url(self, user_url):
        start = user_url.find('=') + 1
        end = user_url.find('&')
        return user_url[start:end]

    def spider_do(self, home_page):
        """
        Go to the gossip page, get gossips.
        :param home_page:
        :return:
        """

        # Go to personal page
        personal_page_soup = None
        gossip_page_url = ''

        home_page_soup = bs4.BeautifulSoup(home_page, 'lxml')
        for child in home_page_soup.descendants:
            if child.name == 'a' and child.string == '个人主页':
                personal_page = urllib2.urlopen(child['href']).read()
                personal_page_soup = bs4.BeautifulSoup(personal_page, 'lxml')
                break

        # Get the gossip page url as a spider start
        if personal_page_soup is None:
            return

        for child in personal_page_soup.descendants:
            if child.name == 'a' and child.string == '留言板':
                gossip_page_url = child['href']
                break

        # # Open local web page for test.
        # soup = bs4.BeautifulSoup(open(r'TestFile/gossip_page.html'), 'lxml')

        total_pages_count = self.get_total_pages_count(gossip_page_url)

        print 'Start: ', time.strftime('%H:%M:%S', time.localtime(time.time()))

        # Get gossips, maybe a generator is a better solution for functional programming.

        # senders = {}  # A dict to collect all senders.

        page_idx = 0
        while gossip_page_url != '':
            gossip_page = urllib2.urlopen(gossip_page_url).read()
            soup = bs4.BeautifulSoup(gossip_page, 'lxml')
            gossips_tag = soup.find(class_="list")
            for child in gossips_tag.children:
                if child.p is not None:
                    if '李修竹' in str(child.get_text()):
                        print child
                elif child.a.string == '下一页':  # is next page
                    gossip_page_url = child.a['href']
                else:  # is last page
                    gossip_page_url = ''

            page_idx += 1
            print '%.2f%%' % (page_idx / float(total_pages_count) * 100)

        print 'End: ', time.strftime('%H:%M:%S', time.localtime(time.time()))

        # for k, v in senders.iteritems():
        #     print '{0} : {1}'.format(k, v)

if __name__ == '__main__':
    config = Config.Config()
    config.init_config_from_file(r'C:\config.txt')

    spider = RenrenSpider(config.username, config.pwd, login_domain)
    spider.spider_do(spider.login())


