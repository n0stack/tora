# coding:UTF-8

import libvirt
import os
import re

QEMU_URL = "qemu:///system"

class VMInfo:

    def __init__(self):
        pass


    def connect_to_qemu(self):
        conn = libvirt.openReadOnly(QEMU_URL)

        if conn == None:
            print 'Failed to connection to the hypervisor'
            sys.exit(1)


    def show_domain_all(self):
        domains = conn.listDefinedDomains()
        print (domains)

        
