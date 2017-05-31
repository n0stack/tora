# coding: UTF-8
import time
import libvirt
import enum
from kvmconnect.base import BaseOpen
from operation.xmllib.vm import PoolGen

class PoolCreate(BaseOpen):
    def __init__(self):
        super().__init__()

    def __call__(self, pool_name, pool_size, pool_path):
        pool = PoolGen()
        pool(pool_name, pool_size, pool_path)

        status = self.connection.storagePoolCreateXML(pool.xml, 0)

        if not status:
            return {"message": "Failed."}, 422
        else:
            return {"message": "Successful."}, 201
        
