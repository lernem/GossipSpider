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
            config = f.readlines()
            config = map(lambda x: x.strip('\n'), config)

            self.username = config[0]
            self.pwd = config[1]