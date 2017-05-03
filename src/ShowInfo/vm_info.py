# coding:UTF-8
import libvirt
import os
import re
import pprint
import json
from xml.dom import minidom
from Base import BaseReadOnly


class DomainInfo(BaseReadOnly):
    """
    Show VM's information
    """
    
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


    # Domain(VM) name
    def get_domain(self, id):
        domain = self.connection.lookupByID(id)
        return domain.name()


    # VM tatus
    def get_state(self, id):
        domain = self.connection.lookupByID(id)
        return domain.info()[0]


    # VM max memory
    def get_max_memory(self, id):
        domain = self.connection.lookupByID(id)
        return domain.info()[1]


    # Number of CPU
    def get_CPU_number(self, id):
        domain = self.connection.lookupByID(id)
        return domain.info()[3]


    # CPU time
    def get_CPU_time(self, id):
        domain = self.connection.lookupByID(id)
        return domain.info()[2]


    # Domain's XML(settings)
    def get_domain_XML(self, id):
        domain = self.connection.lookupByID(id)
        return minidom.parseString(domain.XMLDesc(0))


    # All information
    def show_domain_info_all(self):
        domain = []
        for id in self.connection.listDomainsID():
            
            _information = {"id": id,
                            "name": self.get_domain(id),
                            "state": self.get_state(id),
                            "max_memory": self.get_max_memory(id),
                            "number_of_CPU": self.get_CPU_number(id),
                            "CPU_time": self.get_CPU_time(id)}
            
            # Read XML file
            domain_XML = self.get_domain_XML(id)
            _interfaces = []
            # Show interface's information
            for iface in domain_XML.getElementsByTagName("interface"):
                _interfaces.append(self.get_domain_network_info(iface))
            _information.update({"interfaces": _interfaces})

            domain.append(_information)

        return json.dumps(domain)


    # for debug
    def get_domain_network_info(self, iface):
        network_info = {"interface_type": iface.getAttribute('type'),
                        "network": self.get_network(iface),
                        "bridge": self.get_bridge(iface),
                        "mac_address": self.get_mac(iface),
                        "device": self.get_device(iface)}

        return network_info


# for debug
api = DomainInfo()
print (api.show_domain_info_all())
