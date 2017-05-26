# coding: UTF-8
import time
import libvirt
from kvmconnect.base import BaseOpen
from operation.xmllib.vm import VmGen
from operation.xmllib.pool import PoolGen


class VmOperation(BaseOpen):
    """
    about vm
    """
    def __init__(self):
        super().__init__()

    def start_vm(self, name):
        domain = self.connection.lookupByName(name)
        domain.create()

        # Return failed if 60s spent.
        s = time.time()
        while True:
            if domain.info()[0] == 1:
                break
            if time.time() - s > 120:
                return {"state": "failed"}, 422

        return {"state": "successful"}, 200

    def stop_vm(self, name):
        domain = self.connection.lookupByName(name)
        domain.shutdown()

        # Return failed if 60s spent.
        s = time.time()
        while True:
            if domain.info()[0] != 1:
                break
            if time.time() - s > 120:
                return {"state": "failed"}, 422

        return {"state": "successful"}, 200


    def force_stop_vm(self, name):
        domain = self.connection.lookupByName(name)
        domain.destroy()

        # Return failed if 60s spent.
        s = time.time()
        while True:
            if domain.info()[0] != 1:
                break
            if time.time() - s > 60:
                return {"state": "failed"}, 422

        return {"state": "successful"}, 200


class VmCreate(BaseOpen):
    """
    Create VM
    """

    def __init__(self):
        super().__init__()

    def __call__(self, name, boot, cdrom, memory_size, vcpu_num):
        vm = VmGen()
        vm(name, boot, cdrom, memory_size, vcpu_num)

        dom = self.connection.createXML(vm.xml, 0)
        dom = self.connection.defineXML(vm.xml)
        
        if not dom:
            return {"message": "Connot create."}, 422
        else:
            return {"message": "Successful."}, 201


class PoolCreate(BaseOpen):
    def __init__(self):
        super().__init__()

    def __call__(self, pool_name, pool_size, pool_path):
        pool = PoolGen()
        pool(pool_name, pool_size, pool_path)

        status = self.connection.storagePoolCreateXML(xml, 0)
        
        if not status:
            return {"message": "Failed."}, 422
        else:
            return {"message": "Successful."}, 201
