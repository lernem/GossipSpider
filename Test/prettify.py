#! /usr/bin/env python
# coding:utf-8

import bs4
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    soup = bs4.BeautifulSoup(open(r'TestFile\multi_emoji.html'), 'lxml')

    with open(r'TestFile\multi_emoji_pretty.html', 'w') as f:
        f.write(soup.prettify())

