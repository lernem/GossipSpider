#! /usr/bin/env python
# coding:utf-8

import bs4
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def enum_elem(elem, recur_time=0):
    recur_time += 1
    print '--- enter enum_elem ---', recur_time
    if type(elem) is bs4.element.NavigableString:
        print '--- out enum_elem ---', recur_time
        return

    for child in elem.children:
        print 222
        print type(child), child
        if type(child) is not bs4.element.NavigableString:
            enum_elem(child, recur_time)
    print '--- out enum_elem ---', recur_time


def generate_gossip(soup):
    tmptag = soup.find(class_='list')
    if tmptag is None:
        return None

    for gossip_data in tmptag:
        print '================================'
        print 333
        enum_elem(gossip_data)
        return None

if __name__ == '__main__':
    soup = bs4.BeautifulSoup(open('Multi_emoji.html'), 'lxml')

    generate_gossip(soup)

