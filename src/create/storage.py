# coding: UTF-8
from sml.etree.ElementTree import Element, SubElement
import xml.etree.ElementTree as ET
import uuid
import libvirt
from create import utils
from kvmconnect.base import BaseOpen


class CreateStorage(BaseOpen):
    """
    Create pool and storage
    """

    def __init__(self):
        super().__init__()

    def __call__(self):
        xmlDesc = """
        <pool type='dir'>
        <name>mypool</name>
        <uuid>1111</uuid>
        <capacity unit='bytes'>1930</capacity>
        <allocation unit='bytes'>1000</allocation>
        <available unit='bytes'>930</available>
        <source>
        </source>
        <target>
        <path>/home/aiueo/images</path>
        <permissions>
        <mode>0755</mode>
        <owner>-1</owner>
        <group>-1</group>
        </permissions>
        </target>
        </pool>"""

        # create pool
        pool = self.connection.storagePoolCreateXML(xmlDesc, 0)
        
        
