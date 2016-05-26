#! /usr/bin/env python
# coding:utf-8

import bs4
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def enum_elem(elem, recur_indent=''):
    recur_indent += '  --  '
    if type(elem) is bs4.element.NavigableString:
        return

    for child in elem.children:
        print recur_indent, type(child), child.name, ' ## (', child, ')'
        if type(child) is not bs4.element.NavigableString:
            enum_elem(child, recur_indent)


def generate_gossip(soup):
    tmptag = soup.find(class_='list')
    if tmptag is None:
        return None

    for gossip_data in tmptag:
        print '================================'
        enum_elem(gossip_data)
        # print(gossip_data)

if __name__ == '__main__':
    soup = bs4.BeautifulSoup(open('Multi_emoji.html'), 'lxml')

    generate_gossip(soup)

