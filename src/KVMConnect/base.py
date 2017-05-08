# coding:UTF-8
import libvirt
import os
import re
import sys
from xml.dom import minidom


class BaseReadOnly:

    def __init__(self):
        self.QEMU_URL = "qemu:///system"
        self.connect_to_qemu()


    def connect_to_qemu(self):
        self.connection = libvirt.openReadOnly(self.QEMU_URL)
        if self.connection == None:
            print ("Failed to connect to the hypervisor.")
            sys.exit(1)

        
class BaseOpen:
    
    def __init__(self):
        self.QEMU_URL = "qemu:///system"
        self.connect_to_qemu()


    def connect_to_qemu(self):
        self.connection = libvirt.open(self.QEMU_URL)
        if self.connection == None:
            print ("Failed to connect to the hypervisor.")
            sys.exit(1)


