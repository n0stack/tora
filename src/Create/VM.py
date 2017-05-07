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

    def getXML(self):
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


        self.getXML()
        #vm = self.connection.lookupByName(vm_name)

        # domain tag
        domain = Element('domain', attrib={'type':'qemu'})
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
        devices = self.devices(boot, cdrom)
        domain.append(name)
        domain.append(uuid)
        domain.append(description)
        domain.append(memory)
        domain.append(currentMemory)
        domain.append(vcpu)
        domain.append(self.os)
        domain.append(devices)

        xml = ET.tostring(domain).decode('utf-8').replace('\n', '')
        print (xml)
        #dom = self.connection.createXML(xml, 0)
        #dom = self.connection.defineXML(xml)


        
        
        
    def devices(self, boot, cdrom):
        text = """
        <devices>
        <emulator>/usr/bin/qemu-system-x86_64</emulator>
        <disk type='file' device='disk'>
        <driver name='qemu' type='qcow2'/>
        <source file='%s'/>
        <target dev='hda' bus='ide'/>
        <address type='drive' controller='0' bus='0' target='0' unit='0'/>
        </disk>
        <disk type='file' device='cdrom'>
        <source file='%s'>
        <driver name='qemu' type='raw'/>
        <target dev='hdb' bus='ide'/>
        <readonly/>
        <address type='drive' controller='0' bus='0' target='0' unit='1'/>
        </disk>
        <controller type='usb' index='0' model='ich9-ehci1'>
        <address type='pci' domain='0x0000' bus='0x00' slot='0x05' function='0x7'/>
        </controller>
        <interface type='bridge'>
        <mac address='52:54:00:93:1e:ee'/>
        <source bridge='br0'/>
        <model type='rtl8139'/>
        <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0' />
        </interface>
        <serial type='pty'>
        <target port='0'/>
        </serial>
        <console type='pty'>
        <target type='serial' port='0'/>
        </console>
        <input type='mouse' bus='ps2'/>
        <input type='keyboard' bus='ps2'/>
        <graphics type='vnc' port='-1' autoport='yes' listen='0.0.0.0' passwd='vnc'>
        <listen type='address' address='0.0.0.0'/>
        </graphics>
        <video>
        <model type='cirrus' vram='16384' heads='1'/>
        <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x0'/>
        </video>
        <memballoon model='virtio'>
        <address type='pci' domain='0x0000' bus='0x00' slot='0x04' function='0x0'/>
        </memballoon>
        </devices>
        """ % (boot, cdrom)
        return ET.XML(text)

