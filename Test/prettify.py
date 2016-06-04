#! /usr/bin/env python
# coding:utf-8

import bs4
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def prettify_html(path, output_path):
    soup = bs4.BeautifulSoup(open(path), 'lxml')

    with open(output_path, 'w') as f:
        f.write(soup.prettify())

if __name__ == '__main__':
    # prettify_html()
    pass

