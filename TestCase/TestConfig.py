#! /usr/bin/env python
# coding:utf-8

import unittest
import Config
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class TestConfig(unittest.TestCase):
    def test_read(self):
        config = Config.Config()
        config.init_config_from_file(r'C:\config.txt')
        # self.assertEqual('lernem@126.com', config.username)
        # self.assertEqual('Feed3)one)))', config.pwd)


if __name__ == '__main__':
    unittest.main()
