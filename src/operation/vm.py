# coding: UTF-8
import time
import libvirt
import enum
from kvmconnect.base import BaseOpen
from operation.xmllib.vm import VmGen
from operation.xmllib.pool import PoolGen


class Status(BaseOpen):
    """
    manage vm status
    """

    status = enum.Enum('status', 'poweroff running')

    def __init__(self):
        super().__init__()

    def info(self):
        """Return status of vm
        """
        pass

    def start(self, name):
        domain = self.connection.lookupByName(name)
        try:
            domain.create()
        except:
            return False

        # fail if over 120 seconds
        s = time.time()
        while True:
            if domain.info()[0] == 1:
                break
            if time.time() - s > 120:
                return False

        return True

    def stop(self, name):
        domain = self.connection.lookupByName(name)
        domain.shutdown()

        # fail if over 120 seconds
        s = time.time()
        while True:
            if domain.info()[0] != 1:
                break
            if time.time() - s > 120:
                return False

        return True

    def force_stop(self, name):
        domain = self.connection.lookupByName(name)
        domain.destroy()

        # fail if over 60 seconds
        s = time.time()
        while True:
            if domain.info()[0] != 1:
                break
            if time.time() - s > 60:
                return False

        return True


class Create(BaseOpen):
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
            return False
        else:
            return True


class Delete(BaseOpen):
    """
    Delete VM
    """
    def __init__(self):
        super().__init__()

    def __call__(self, name):
        try:
            vdom = self.connection.lookupByName(name)
            vdom.destroy()
            vdom.undefine()
        except:
            return False

        return True


