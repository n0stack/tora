# coding: UTF-8
from xml.etree.ElementTree import Element, SubElement
import xml.etree.ElementTree as ET
import uuid
import libvirt
from create import utils
from kvmconnect.base import BaseOpen


class VmGen:
    """
    Create VM
    """

    def __init__(self):
        pass

    def __call__(self, name, boot, cdrom, memory_size, vcpu_num):
        self.vm_name = name
        self.boot = boot
        self.cdrom = cdrom
        self.memory_size = memory_size
        self.vcpu_num = vcpu_num

        # domain tag
        domain = Element('domain', attrib={'type': 'qemu'})

        # name tag
        name = Element('name')
        name.text = self.vm_name

        # uuid tag
        uuid = Element('uuid')
        uuid.text = utils.randomUUID()

        # description tag
        description = Element('description')
        description.text = "test description"

        # memory tag
        memory = Element('memory', attrib={'unit': 'KiB'})
        memory.text = str(self.memory_size)

        # current memory tag
        currentMemory = Element('currentMemory', attrib={'unit': 'KiB'})
        currentMemory.text = str(self.memory_size)

        # vcpu tag
        vcpu = Element('vcpu', attrib={'placement': 'static'})
        vcpu.text = str(self.vcpu_num)

        # os tag
        self.create_os_tag()

        # devices tag
        self.create_devices_tag()

        # Create XML file and append some tags
        domain.append(name)
        domain.append(uuid)
        domain.append(description)
        domain.append(memory)
        domain.append(currentMemory)
        domain.append(vcpu)
        domain.append(self.os)
        domain.append(self.devices)

        self.xml = ET.tostring(domain).decode('utf-8').replace('\n', '')

    def create_os_tag(self):
        self.os = Element('os')

        # Decide arch
        type = Element('type', attrib={'arch': 'x86_64'})
        type.text = 'hvm'

        boot1 = Element('boot', attrib={'dev': 'cdrom'})
        boot2 = Element('boot', attrib={'dev': 'hd'})

        self.os.append(type)
        self.os.append(boot1)
        self.os.append(boot2)

    def create_devices_tag(self):
        self.devices = Element('devices')

        # emulator tag
        self.emulator = Element('emulator')
        self.emulator.text = "/usr/bin/qemu-system-x86_64"

        # disk1 tag
        self.create_qcow2_tag()

        # disk2 tag(cdrom)
        self.create_iso_tag()

        # controller1 tag
        self.controller1 = Element('controller', attrib={'type': 'usb',
                                                    'index': '0',
                                                    'model': 'ich9-ehci1'})
        address = Element('address', attrib={'type': 'pci',
                                             'domain': '0x0000',
                                             'bus': '0x00',
                                             'slot': '0x05',
                                             'function': '0x7'})
        self.controller1.append(address)

        # controller2 tag
        self.controller2 = Element('controller', attrib={'type': 'usb',
                                                    'index': '0',
                                                    'model': 'ich9-uhci1'})
        master = Element('master', attrib={'startport': '0'})
        address = Element('address', attrib={'type': 'pci',
                                             'domain': '0x0000',
                                             'bus': '0x00',
                                             'slot': '0x05',
                                             'function': '0x0',
                                             'multifunction': 'on'})
        self.controller2.append(master)
        self.controller2.append(address)

        # interface1 tag
        self.interface1 = Element('interface', attrib={'type': 'bridge'})
        mac = Element('mac', attrib={'address': '52:54:00:43:e0:a0'})
        source = Element('source', attrib={'bridge': 'br0'})
        model = Element('model', attrib={'type': 'virtio'})
        address = Element('address', attrib={'type': 'pci',
                                             'domain': '0x0000',
                                             'bus': '0x00',
                                             'slot': '0x02',
                                             'function': '0x0'})
        self.interface1.append(mac)
        self.interface1.append(source)
        self.interface1.append(model)
        self.interface1.append(address)

        # serial tag
        self.serial = Element('serial', attrib={'type': 'pty'})
        target = Element('target', attrib={'port': '0'})
        self.serial.append(target)

        # console tag
        self.console = Element('console', attrib={'type': 'pty'})
        target = Element('target', attrib={'type': 'serial',
                                           'port': '0'})
        self.console.append(target)

        # channel tag
        self.channel = Element('channel', attrib={'type': 'unix'})
        source = Element('source', attrib={'mode': 'bind'})
        target = Element('target', attrib={'type': 'virtio',
                                           'name': 'org.qemu.guest_agent.0'})
        address = Element('address', attrib={'type': 'virtio-serial',
                                             'controller': '0',
                                             'bus': '0',
                                             'port': '1'})
        self.channel.append(source)
        self.channel.append(target)
        self.channel.append(address)

        # input tag
        self.input = Element('input', attrib={'type': 'tablet',
                                         'bus': 'usb'})

        # memballoon tag
        self.memballoon = Element('memballoon', attrib={'model': 'virtio'})
        address = Element('address', attrib={'type': 'pci',
                                             'domain': '0x0000',
                                             'bus': '0x00',
                                             'slot': '0x07',
                                             'function': '0x0'})
        self.memballoon.append(address)


        self.devices.append(self.emulator)
        self.devices.append(self.disk1)
        self.devices.append(self.disk2)
        self.devices.append(self.controller1)
        self.devices.append(self.controller2)
        self.devices.append(self.interface1)
        self.devices.append(self.serial)
        self.devices.append(self.console)
        self.devices.append(self.channel)
        self.devices.append(self.input)
        self.devices.append(self.memballoon)

    def create_qcow2_tag(self):
        self.disk1 = Element('disk', attrib={'type': 'file', 'device': 'disk'})
        driver = Element('driver', attrib={'name': 'qemu', 'type': 'qcow2'})
        source = Element('source', attrib={'file': self.boot})
        target = Element('target', attrib={'dev': 'vda', 'bus': 'virtio'})
        address = Element('address', attrib={'type': 'pci',
                                             'domain': '0x0000',
                                             'bus': '0x00',
                                             'slot': '0x06',
                                             'function': '0x0'})
        self.disk1.append(driver)
        self.disk1.append(source)
        self.disk1.append(target)
        self.disk1.append(address)

    def create_iso_tag(self):
        self.disk2 = Element('disk', attrib={'type': 'file', 'device': 'cdrom'})
        driver = Element('driver', attrib={'name':'qemu', 'type': 'raw'})
        source = Element('source', attrib={'file': self.cdrom})
        target = Element('target', attrib={'bus': 'ide', 'dev': 'hdb'})
        read_only = Element('readonly')
        address = Element('address', attrib={'bus': '0',
                                             'controller': '0',
                                             'target': '0',
                                             'type': 'drive',
                                             'unit': '1'})
        self.disk2.append(driver)
        self.disk2.append(source)
        self.disk2.append(target)
        self.disk2.append(read_only)
        self.disk2.append(address)

