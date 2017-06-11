# coding: UTF-8
from kvmconnect.base import BaseOpen
from operation.xmllib.volume import VolumeGen

import os


class Create(BaseOpen):
    def __init__(self):
        super().__init__()

    def __call__(self, pool_name, volume_name, size):
        volume = VolumeGen()
        volume(volume_name, size)

        try:
            pool = self.connection.storagePoolLookupByName(pool_name)
            status = pool.createXML(pool.xml)
        except:
            return False

        if not status:
            return False
        else:
            return True
        

class Delete(BaseOpen):
    def __init__(self):
        super().__init__()

    def __call__(self, pool_name, volume_name):
        try:
            pool = self.connection.storagePoolLookupByName(pool_name)
            storage = pool.storageVolLookupByName(volume_name)
            storage.delete()
        except:
            return False

        return True
