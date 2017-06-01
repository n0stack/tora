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
            return {"message": "Failed."}, 422

        if not status:
            return {"message": "Failed."}, 422
        else:
            return {"message": "Successful."}, 201
        

class Delete(BaseOpen):
    def __init__(self):
        super().__init__()

    def __call__(self, pool_name, volume_name):
        try:
            pool = self.connection.storagePoolLookupByName(pool_name)
            storage = pool.storageVolLookupByName(volume_name)
            storage.delete()
        except:
            return {"message": "Failed."}, 422

        return {"message": "Successful."}, 201
