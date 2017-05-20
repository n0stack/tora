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
        time.sleep(10)

        if domain.info()[0] != "1":
            return {"state": "failed"}
        return {"state": "successful"}

    def stop_vm(self, name):
        domain = self.connection.lookupByName(name)
        domain.shutdown()
        s = time.time()
        # Return failed if 60s spent.
        while True:
            if domain.info()[0] == "0":
                break
            if time.time() - s > 60:
                return {"state": "failed"}

        return {"state": "successful"}


    def force_stop_vm(self, name):
        domain = self.connection.lookupByName(name)
        domain.destroy()
        time.sleep(10)

        if domain.info()[0] != "0":
            return {"state": "failed"}
        return {"state": "successful"}


