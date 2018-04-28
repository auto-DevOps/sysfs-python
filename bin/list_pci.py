#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   list_pci.py
Author:     Fasion Chan
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''

from sysfs.bus.pci.device import(
    PCIDevice,
)

for pci in PCIDevice.iter():
    print(pci)
    print('')
