# coding: UTF-8
from xml.etree.ElementTree import Element, SubElement
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

    def __call__(self, pool_name, pool_size, pool_path):
        
        pool = Element('pool', attrib={'type': 'dir'})
        name = Element('name')
        name.text = pool_name

        uuid = Element('uuid')
        uuid.text = utils.randomUUID()

        capacity = Element('capacity', attrib={'unit': 'bytes'})
        capacity.text = str(pool_size)
        allocation = Element('allocation', attrib={'unit': 'bytes'})
        allocation.text = '0'
        available = Element('allocation', attrib={'unit': 'bytes'})
        available.text = str(int(capacity.text) - int(allocation.text))
        
        source = Element('source')
        target = Element('target')
        path = Element('path')
        path.text = pool_path

        permissions = Element('permission')
        mode = Element('mode')
        mode.text = '0755'
        owner = Element('owner')
        owner.text = '-1'
        group = Element('group')
        group.text = '-1'

        permissions.append(mode)
        permissions.append(owner)
        permissions.append(group)
                
        target.append(path)
        target.append(permissions)

        pool.append(name)
        pool.append(uuid)
        pool.append(capacity)
        pool.append(allocation)
        pool.append(available)
        pool.append(source)
        pool.append(target)

        xml = ET.tostring(pool).decode('utf-8').replace('\n', '')
        print(xml)
        # create pool
        pool_success = self.connection.storagePoolCreateXML(xml, 0)
        
        
