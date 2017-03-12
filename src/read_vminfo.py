# coding:UTF-8

import libvirt
import os
import re

QEMU_URL = "qemu:///system"

class VMInfo:

    def __init__(self):
        pass


    def connect_to_qemu(self):
        self.connection = libvirt.openReadOnly(QEMU_URL)

        if self.connection == None:
            print ("Failed to connect to the hypervisor")
            sys.exit(1)

        print ("Success to connect to the hypervisor")


    def show_domain_all(self):
        domains = self.connection.listDefinedDomains()
        print (domains)


    # Show all domain's all information(id,name,state...)
    def show_domain_info_all(self):
        for id in self.connection.listDomainsID():
            domain = self.connection.lookupByID(id)
            info = domain.info()
            print ("ID = {}".format(id))
            print ("Name = {}".format(domain.name()))
            print ("State = {}".format(info[0]))
            print ("Max Memory = {}".format(info[1]))
            print ("Number of CPUs = {}".format(info[3]))
            print ("CPU time = {}".format(info[2]))            




# for debug
vm = VMInfo()
vm.connect_to_qemu()
vm.show_domain_info_all()
