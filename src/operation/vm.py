# coding: UTF-8
import libvirt
from kvmconnect.base import BaseOpen
import time

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

