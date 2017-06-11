# coding: UTF-8
import time
import libvirt
import enum
from kvmconnect.base import BaseOpen
from operation.xmllib.vm import VmGen
from operation.xmllib.pool import PoolGen
from operation.volume import Create as VolCreate
from operation.volume import Delete as VolDelete


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

    parameters:
        name: VM (domain) name
        cpu: 
            arch: cpu architecture
            nvcpu: number of vcpus
        memory: memory size of VM
        disk:
            pool: pool name where disk is stored
            size: volume size
        cdrom: iso image path
        mac_addr: mac address
        vnc_password: vnc password

    """
    def __init__(self):
        super().__init__()

    def __call__(self, name, cpu, memory, disk, cdrom, mac_addr, vnc_password):
        vmgen = VmGen()

        # create volume (disk)
        volcreate = VolCreate()
        if not volcreate(disk['pool'], name, disk['size']):
            return False

        # default values of nic
        nic = {'type': 'bridge', 'source': 'virbr0', 'mac_addr': mac_addr, 'model': 'virtio'}

        pool = self.connection.storagePoolLookupByName(disk['pool'])
        vol = pool.storageVolLookupByName(name+'.img')

        vmgen(name, cpu, memory, vol.path(), cdrom, nic, vnc_password)

        dom = self.connection.createXML(vmgen.xml, 0)
        
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
            if vdom.isActive(): # vm is up
                vdom.destroy()
            else:
                vdom.undefine()

            # delete matched volume
            for pool in self.connection.listAllStoragePools():
                for vol in pool.listAllVolumes():
                    if vol.name() == name+'.img':
                        vol.delete()
                    
        except libvirt.libvirtError as e:
            print(e)
            return False

        return True


