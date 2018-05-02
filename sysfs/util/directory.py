#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   directory.py
Author:     Fasion Chan
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''

import os


class DirectoryMixin(object):

    def read_file(self, name, mode='rb'):
        path = os.path.join(self.path, name)
        return open(path, mode).read()

    def read_bytes(self, name):
        return self.read_file(name=name, mode='rb')

    def read_string(self, name):
        return self.read_file(name=name, mode='r')

    def read_int(self, name, base=10):
        return int(self.read_string(name=name), base)

    def read_decimal(self, name):
        return self.read_int(name=name, base=10)

    def read_hexadecimal(self, name):
        return self.read_int(name=name, base=16)
