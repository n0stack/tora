# coding: UTF-8
from kvmconnect.base import BaseOpen
from operation.xmllib.pool import PoolGen

import os


class Create(BaseOpen):
    def __init__(self):
        super().__init__()

    def __call__(self, pool_name="tora", pool_path="$HOME/pool"):
        path = os.path.expandvars(pool_path)
        if not os.path.exists(path):
            try:
                os.mkdir(path)
            except PermissionError:
                return False

        pool = PoolGen()
        pool(pool_name, path)

        status = self.connection.storagePoolDefineXML(pool.xml, 0)

        if not status:
            return False
        else:
            return True
        

class Delete(BaseOpen):
    def __init__(self):
        super().__init__()

    def __call__(self, name):
        try:
            pool = self.connection.storagePoolLookupByName(name)
            pool.undefine()
        except:
            return False

        return True
