from xml.etree.ElementTree import Element, SubElement
import xml.etree.ElementTree as ET
import uuid
from Create import utils
from KVMConnect.Base import BaseOpen


class CreateVM(BaseOpen):
    """
    Create VM
    """

    def __init__(self):
        super().__init__()

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

    def create_vm(self):
        boot = "cent1.img"
        cdrom = "/home/palloc/iso_file/CentOS-7-x86_64-Minimal-1611.iso"
        vm_name = "cent1"

        # Check the existence of VM
        try:
            vm = self.connection.lookupByName(vm_name)
        except libvirt.libvirtError:
            pass
        if vm is not None:
            return None

        # domain tag
        domain = Element('domain', attrib={'type': 'qemu'})

        # os tag
        self.create_os_tag()

        # name tag
        name = Element('name')
        name.text = vm_name

        # uuid tag
        uuid = Element('uuid')
        uuid.text = utils.randomUUID()

        # description tag
        description = Element('description')
        description.text = "test description"

        # memory tag
        memory = Element('memory', attrib={'unit': 'KiB'})
        memory.text = "256"

        # current memory tag
        currentMemory = Element('currentMemory', attrib={'unit': 'KiB'})
        currentMemory.text = "256"

        # vcpu tag
        vcpu = Element('vcpu', attrib={'placement': 'static'})
        vcpu.text = "1"

        # Create XML file and append some tags
        self.create_devices(boot, cdrom)
        domain.append(name)
        domain.append(uuid)
        domain.append(description)
        domain.append(memory)
        domain.append(currentMemory)
        domain.append(vcpu)
        domain.append(self.os)
        domain.append(self.devices)

        xml = ET.tostring(domain).decode('utf-8').replace('\n', '')
        print(xml)
        dom = self.connection.createXML(xml, 0)
        dom = self.connection.defineXML(xml)

    def create_devices(self, boot, cdrom):
        self.devices = Element('devices')

        # emulator tag
        emulator = Element('emulator')
        emulator.text = "/usr/bin/qemu-system"

        # disk1 tag
        disk1 = Element('disk', attrib={'type': 'file', 'device': 'disk'})

        driver = Element('driver', attrib={'name': 'qemu', 'type': 'qcow2'})
        source = Element('source', attrib={'file': boot})
        target = Element('target', attrib={'dev': 'vda', 'bus': 'virtio'})
        address = Element('address', attrib={'type': 'pci',
                                             'domain': '0x0000',
                                             'bus': '0x00',
                                             'slot': '0x06',
                                             'function': '0x0'})
        disk1.append(driver)
        disk1.append(source)
        disk1.append(target)
        disk1.append(address)

        # controller1 tag
        controller1 = Element('controller', attrib={'type': 'usb',
                                                    'index': '0',
                                                    'model': 'ich9-ehci1'})
        address = Element('address', attrib={'type': 'pci',
                                             'domain': '0x0000',
                                             'bus': '0x00',
                                             'slot': '0x05',
                                             'function': '0x7'})
        controller1.append(address)

        # controller2 tag
        controller2 = Element('controller', attrib={'type': 'usb',
                                                    'index': '0',
                                                    'model': 'ich9-uhci1'})
        master = Element('master', attrib={'startport': '0'})
        address = Element('address', attrib={'type': 'pci',
                                             'domain': '0x0000',
                                             'bus': '0x00',
                                             'slot': '0x05',
                                             'function': '0x0',
                                             'multifunction': 'on'})
        controller2.append(master)
        controller2.append(address)

        # interface1 tag
        interface1 = Element('interface', attrib={'type': 'bridge'})
        mac = Element('mac', attrib={'address': '52:54:00:43:e0:a0'})
        source = Element('source', attrib={'bridge': 'br0'})
        model = Element('model', attrib={'type': 'virtio'})
        address = Element('address', attrib={'type': 'pci',
                                             'domain': '0x0000',
                                             'bus': '0x00',
                                             'slot': '0x02',
                                             'function': '0x0'})
        interface1.append(mac)
        interface1.append(source)
        interface1.append(model)
        interface1.append(address)

        # serial tag
        serial = Element('serial', attrib={'type': 'pty'})
        target = Element('target', attrib={'port': '0'})
        serial.append(target)

        # console tag
        console = Element('console', attrib={'type': 'pty'})
        target = Element('target', attrib={'type': 'serial',
                                           'port': '0'})

        # channel tag
        channel = Element('channel', attrib={'type': 'unix'})
        source = Element('source', attrib={'mode': 'bind'})
        target = Element('target', attrib={'type': 'virtio',
                                           'name': 'org.qemu.guest_agent.0'})
        address = Element('address', attrib={'type': 'virtio-serial',
                                             'controller': '0',
                                             'bus': '0',
                                             'port': '1'})
        channel.append(source)
        channel.append(target)
        channel.append(address)

        # input tag
        input = Element('input', attrib={'type': 'tablet',
                                         'bus': 'usb'})

        # memballoon tag
        memballoon = Element('memballoon', attrib={'model': 'virtio'})
        address = Element('address', attrib={'type': 'pci',
                                             'domain': '0x0000',
                                             'bus': '0x00',
                                             'slot': '0x07',
                                             'function': '0x0'})
        memballoon.append(address)

        self.devices.append(emulator)
        self.devices.append(disk1)
        self.devices.append(controller1)
        self.devices.append(controller2)
        self.devices.append(interface1)
        self.devices.append(serial)
        self.devices.append(console)
        self.devices.append(channel)
        self.devices.append(input)
        self.devices.append(memballoon)
