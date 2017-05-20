# coding: UTF-8
import libvirt
from kvmconnect.base import BasdeOpen
import time

class VmOperate(self):
    """
    about vm
    """
    def __init__(self):
        super().__init__()

    def start_vm(self, id):
        domain = self.connection.lookupByID(id)
        domain.create()
        time.sleep(10)

        if domain.info()[0] != "1":
            return {"state": "failed"}
        return {"state": "successful"}

