#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   device.py
Author:     Fasion Chan
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''

import os

from collections import (
    OrderedDict,
)


class PCIDevice(OrderedDict):

    DEVICES_PATH = '/sys/bus/pci/devices'

    PCI_IDS = None
    PCI_CLASSES = None

    try:
        from pciutil import (
            PciIds,
            PciClasses,
        )
        PCI_IDS = PciIds.load_from_system()
        PCI_CLASSES = PciClasses()
    except:
        pass

    @staticmethod
    def load_hex_from_file(path):
        return int(open(path).read(), 16)

    @classmethod
    def iter(cls, ids=PCI_IDS, classes=PCI_CLASSES):
        if not os.path.isdir(cls.DEVICES_PATH):
            return

        for ident in os.listdir(cls.DEVICES_PATH):
            yield cls(
                ident=ident,
                ids=ids,
                classes=classes,
            )

    FIELD_IDENT = 'ident'
    FIELD_CLASS = 'class'
    FIELD_VENDOR = 'vendor'
    FIELD_DEVICE = 'device'
    FIELD_SUBSYSTEM_NAME = 'subsystem_name'

    FIELD_CLASS_ID = 'class_id'
    FIELD_SUBCLASS_ID = 'subclass_id'
    FIELD_INTERFACE_ID = 'interface_id'

    FIELD_CLASS_NAME = 'class_name'
    FIELD_SUBCLASS_NAME = 'subclass_name'
    FIELD_INTERFACE_NAME = 'interface_name'


    def __init__(self, ident, ids=PCI_IDS, classes=PCI_CLASSES):
        super(PCIDevice, self).__init__()

        self.path = os.path.join(self.DEVICES_PATH, ident)

        vendor = self.load_hex_value('vendor')
        device = self.load_hex_value('device')
        subsystem_vendor = self.load_hex_value('subsystem_vendor')
        subsystem_device = self.load_hex_value('subsystem_device')
        subsystem_name = None

        if ids:
            vendor, device, subsystem_name = ids.query(
                vendor=vendor,
                device=device,
                subsystem_vendor=subsystem_vendor,
                subsystem_device=subsystem_device,
            )

        _class = self.load_hex_value('class')

        class_infos = (None,) * 6
        if classes:
            class_infos = classes.query(_class=_class)

        class_id, subclass_id, interface_id, \
            class_name, subclass_name, interface_name = class_infos

        self[self.FIELD_IDENT] = ident

        self[self.FIELD_VENDOR] = vendor
        self[self.FIELD_DEVICE] = device
        self[self.FIELD_SUBSYSTEM_NAME] = subsystem_name

        self[self.FIELD_CLASS] = _class

        self[self.FIELD_CLASS_ID] = class_id
        self[self.FIELD_SUBCLASS_ID] = subclass_id
        self[self.FIELD_INTERFACE_ID] = interface_id

        self[self.FIELD_CLASS_NAME] = class_name
        self[self.FIELD_SUBCLASS_NAME] = subclass_name
        self[self.FIELD_INTERFACE_NAME] = interface_name

    def load_hex_value(self, path):
        return self.load_hex_from_file(path=os.path.join(self.path, path))
