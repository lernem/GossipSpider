#! /usr/bin/env python
# coding:utf-8

import sys


class Config:
    def __init__(self):
        self.username = ''
        self.pwd = ''
        self.target_name = ''

    def init_config_from_file(self, config_file_path):
        with open(config_file_path, 'r') as f:
            lines = f.readlines()

            self.username = lines[0].rstrip()
            self.pwd = lines[1].rstrip()


if __name__ == '__main__':
    config = Config()
    config.init_config_from_file(r'C:\config.txt')
