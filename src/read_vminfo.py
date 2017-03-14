# coding:UTF-8
import libvirt
import os
import re
from xml.dom import minidom
from Base import BaseReadOnly


class DomainInfo(BaseReadOnly):
    """Show VM's information"""
    
    def __init__(self):
        super().__init__()




    # Bridge interface's name
    def get_bridge(self, iface):
        iface_type = iface.getAttribute("type")
        if iface_type == "network":
            net_XML_info = minidom.parseString(Conn.networkLookupByName(network_info).XMLDesc(0))
            bridge = net_XML_info.getElementsByTagName("bridge")[0].getAttribute("name")

        elif iface_type == "bridge":
            bridge = iface.getElementsByTagName("source")[0].getAttribute("bridge")

        else:
            bridge = None

        return bridge

    # Network name
    def get_network(self, iface):
        iface_type = iface.getAttribute("type")
        if iface_type == "network":
            network = iface.getElementsByTagName("source")[0].getAttribute("network")
        else:
            network = None

        return network

    # Mac address
    def get_mac(self, iface):
        return iface.getElementsByTagName("mac")[0].getAttribute("address")

    # Device(nic) name
    def get_device(self, iface):
        return iface.getElementsByTagName("target")[0].getAttribute("dev")


    def get_domain(self, id):
        domain = self.connection.lookupByID(id)
        return domain.name()


    def get_state(self, id):
        domain = self.connection.lookupByID(id)
        return domain.info[0]


    def get_max_memory(self, id):
        domain = self.connection.lookupByID(id)
        return domain.info[1]


    def get_CPU_number(self, id):
        domain = self.connection.lookupByID(id)
        return domain.info[3]


    def get_CPU_time(self, id):
        domain = self.connection.lookupByID(id)
        return domain.info[2]

    

    # for debug
    def show_domain_info_all(self):
        for id in self.connection.listDomainsID():
            print ("-"*30)

            print ("ID = {}".format(id))
            print ("Name = {}".format(self.get_domain(id)))
            print ("State = {}".format(self.get_state(id)))
            print ("Max Memory = {}MB".format(self.get_max_memory(id)))
            print ("Number of CPUs = {}".format(self.get_CPU_number(id)))
            print ("CPU time = {}".format(self.get_CPU_time(id)))

            # Read XML file
            domain_XML = minidom.parseString(domain.XMLDesc(0))

            # Show interface's information
            for iface in domain_XML.getElementsByTagName("interface"):
                self.get_domain_network_info(iface)

            print ("*"*20)
        print ("-"*30)                

    # for debug
    def get_domain_network_info(self, iface):
        print ("*"*20)
        print ("Network = {}".format(self.get_network(iface)))
        print ("Bridge = {}".format(self.get_bridge(iface)))
        print ("Mac address = {}".format(self.get_mac(iface)))
        print ("Device = {}".format(self.get_device(iface)))




# for debug
api = InfoAPI()
api.show_domain_info_all()
