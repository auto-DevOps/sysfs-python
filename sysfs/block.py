#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   block.py
Author:     Fasion Chan
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''

import os

from libase.decorator.property import (
    cached_property,
)

from .util.directory import (
    DirectoryMixin,
)


class BlockDevice(DirectoryMixin):

    SYS_BLOCK_PATH = '/sys/block'
    SECTOR_SIZE = 512

    @classmethod
    def iter(cls):
        for name in os.listdir(cls.SYS_BLOCK_PATH):
            yield cls(name=name)

    def __init__(self, name, path=None):
        self.name = name
        self.path = path or os.path.join(self.SYS_BLOCK_PATH, name)

    @cached_property
    def has_device(self):
        path = os.path.join(self.path, 'device')
        return os.path.exists(path)

    @cached_property
    def dev(self):
        return self.read_string('dev')

    @cached_property
    def device_number(self):
        major, minor = self.dev.split(':')
        return (int(major), int(minor))

    @cached_property
    def major(self):
        return self.device_number[0]

    @cached_property
    def minor(self):
        return self.device_number[1]

    @cached_property
    def size(self):
        return self.SECTOR_SIZE * self.read_decimal('size')

    @cached_property
    def partitions(self):
        return list(self.iter_partitions())

    @cached_property
    def partition(self):
        return self.read_decimal('partition')

    @cached_property
    def model(self):
        model = self.read_string('device/model')
        if model:
            model = model.strip()
        return model

    def iter_partitions(self):
        partitions = []

        for name in os.listdir(self.path):
            if not name.startswith(self.name):
                continue

            path = os.path.join(self.path, name)
            partition_path = os.path.join(path, 'partition')
            if not os.path.exists(partition_path):
                continue

            yield self.__class__(name=name, path=path)
