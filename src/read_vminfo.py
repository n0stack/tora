# coding:UTF-8
import libvirt
import os
import re
from xml.dom import minidom
from Base import BaseReadOnly


class DomainInfo(BaseReadOnly):
    """Show VM or network's information"""
    
    def __init__(self):
        super().__init__()


    # get interface's information
    def get_domain_network_info(self, iface):
        
        print ("*"*20)
        print ("Network device = {}".format(device))
        print ("Bridge = {}".format(bridge))
        print ("Mac address = {}".format(mac_address))
        print ("Network information = {}".format(network_info))


    # Bridge interface's name
    def get_bridge_info(self, iface):
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
    def get_network_info(self, iface):
        iface_type = iface.getAttribute("type")
        if iface_type == "network":
            network = iface.getElementsByTagName("source")[0].getAttribute("network")
        else:
            network = None

        return network

    # Mac address
    def get_mac_info(self, iface):
        return iface.getElementsByTagName("mac")[0].getAttribute("address")

    # Device(nic) name
    def get_device(self, iface):
        return iface.getElementsByTagName("target")[0].getAttribute("dev")





    # Show all domain's all information(id,name,state...)
    def show_domain_info_all(self):
        for id in self.connection.listDomainsID():
            print ("-"*30)

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

            # Show interface's information
            for iface in domain_XML.getElementsByTagName("interface"):
                self.get_domain_network_info(iface)

            print ("*"*20)
        print ("-"*30)                



# for debug
api = InfoAPI()
api.show_domain_info_all()
