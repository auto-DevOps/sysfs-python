#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   list_block_device.py
Author:     Fasion Chan
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''

from sysfs.block import (
    BlockDevice,
)

for device in BlockDevice.iter():
    print(device.name, device.size)
    for partition in device.partitions:
        print(partition.name, partition.partition, partition.size)
    print('')
