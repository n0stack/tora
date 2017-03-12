# coding:UTF-8

import libvirt
import os
import re
from xml.dom import minidom
from .Base import BaseFunc
QEMU_URL = "qemu:///system"


class VMInfo(BaseFunc):

    def __init__(self):
        super().__init__()


    # Show all domain's all information(id,name,state...)
    def show_domain_info_all(self):
        print ("-"*30)
        for id in self.connection.listDomainsID():
            domain = self.connection.lookupByID(id)
            info = domain.info()
            print ("ID = {}".format(id))
            print ("Name = {}".format(domain.name()))
            print ("State = {}".format(info[0]))
            print ("Max Memory = {}MB".format(info[1]/1024))
            print ("Number of CPUs = {}".format(info[3]))
            print ("CPU time = {}".format(info[2]))            

            # Read XML file
            domain_XML = minidom.parseString(domain.XMLDesc(0))

            # print interface's information
            for iface in domain_XML.getElementsByTagName("interface"):
                iface_type = iface.getAttribute("type")

                if iface_type == "network":
                    network_info = iface.getElementsByTagName("source")[0].getAttribute("network")
                    net_XML_info = minidom.parseString(Conn.networkLookupByName(network_info).XMLDesc(0))
                    bridge = net_XML_info.getElementsByTagName("bridge")[ 0 ].getAttribute("name")
                    mac_address = ""
                    device = ""

                elif iface_type == "bridge":
                    network_info = ""
                    bridge = iface.getElementsByTagName("source")[0].getAttribute("bridge")
                    mac_address = iface.getElementsByTagName("mac")[0].getAttribute("address")
                    device = iface.getElementsByTagName("target")[0].getAttribute("dev")

                print ("*"*20)
                print ("Network device = {}".format(device))
                print ("Bridge = {}".format(bridge))
                print ("Mac address = {}".format(mac_address))
                print ("Network information = {}".format(network_info))

            print ("*"*20)
                



# for debug
vm = VMInfo()
vm.show_domain_info_all()
