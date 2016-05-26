#! /usr/bin/env python
# coding:utf-8

import cookielib
import sys
import urllib
import urllib2
import bs4
import time


class Gossip:
    def __init__(self):
        self.sender = ''
        self.receiver = ''
        self.content = ''
        self.time = ''


# Avoid Chinese encoding error.
reload(sys)
sys.setdefaultencoding("utf-8")

# Sign in
login_url = 'http://3g.renren.com/login.do?autoLogin=true'
login_domain = '3g.renren.com'


class Login(object):
    def __init__(self):
        self.name = ''
        self.password = ''
        self.domain = ''
        self.verify_key = ''

        self.cj = cookielib.LWPCookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        urllib2.install_opener(self.opener)

    def set_login_info(self, user_name, pwd, domain, verify_key=''):
        self.name = user_name
        self.password = pwd
        self.domain = domain
        self.verify_key = verify_key

    def get_page_total_cnt(self, gossip_page_url):
        gossip_page = urllib2.urlopen(gossip_page_url).read()
        soup = bs4.BeautifulSoup(gossip_page, 'lxml')
        for child in soup.find(class_="list").children:
            if child.p is None:  # is next page, get total count of pages here
                tmp_lst = [text for text in child.strings]
                tmp_total_str = tmp_lst[5]  # Todo: Need consider about 1 page gossips
                total_str_start_idx = tmp_total_str.find('/') + 1
                total_str_end_idx = tmp_total_str.find('页')
                return int(tmp_total_str[total_str_start_idx:total_str_end_idx])
        return -1

    def login(self):
        # Login
        login_params = {'domain': self.domain, 'email': self.name, 'password': self.password}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'}
        req = urllib2.Request(login_url, urllib.urlencode(login_params), headers=headers)
        response = urllib2.urlopen(req)
        home_page = response.read()

        soup = bs4.BeautifulSoup(home_page, 'lxml')

        # # Write web page to file
        # with open('home_page.html', mode='w') as f:
        #     f.write(soup.prettify())

        # Go to personal page
        for child in soup.descendants:
            if child.name == 'a' and child.string == '个人主页':
                personal_page = urllib2.urlopen(child['href']).read()
                soup = bs4.BeautifulSoup(personal_page, 'lxml')
                break

        # Get the gossip page url as a spider start
        for child in soup.descendants:
            if child.name == 'a' and child.string == '留言板':
                gossip_page_url = child['href']
                break

        # # Open local web page for test.
        # soup = bs4.BeautifulSoup(open('gossip_page.html'), 'lxml')

        # # Write gossip page for local test
        # with open('gossip_page_pretty.html', 'w') as gppf:
        #     gppf.write(soup.prettify())

        total_pages_count = self.get_page_total_cnt(gossip_page_url)

        # Output start time
        print 'Start: ', time.strftime('%H:%M:%S', time.localtime(time.time()))

        # Get gossips, maybe a generator is a better solution for functional programming
        # with open('every_gossip.txt', 'w') as egf:
        page_idx = 0
        while gossip_page_url != '':
            # egf.write(str(page_idx))
            # egf.write('\n')
            page_idx += 1
            print '%.2f%%' % (page_idx / float(total_pages_count) * 100)

            gossip_page = urllib2.urlopen(gossip_page_url).read()
            soup = bs4.BeautifulSoup(gossip_page, 'lxml')
            for child in soup.find(class_="list").children:
                if child.p is not None:  # is gossip
                    # print 'sender:', child.a.string
                    gossip_stuff = child.strings
                    # egf.write(gossip_infs.next() + '\n')
                    content = gossip_stuff.next()
                    content = content.replace('\n', ' ')
                    content = content.replace('\r', ' ')
                    # egf.write(content + '\n')
                    time_str = gossip_stuff.next()
                    if time_str == '悄悄话':
                        time_str = gossip_stuff.next()
                        # egf.write(time_str + '\n')
                elif child.a.string == '下一页':  # is next page
                    # print child.get_text()
                    gossip_page_url = child.a['href']
                else:  # is last page
                    gossip_page_url = ''

                    # egf.write('\n\n')

        # Output end time
        print 'End: ', time.strftime('%H:%M:%S', time.localtime(time.time()))


if __name__ == '__main__':
    user_login = Login()
    username = 'lernem@126.com'
    password = 'Feed3)one)))'
    domain = login_domain
    user_login.set_login_info(username, password, domain)
    user_login.login()
