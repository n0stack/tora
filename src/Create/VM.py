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
        boot = "test2.img"
        cdrom = "/home/palloc/iso_file/mini.iso"
        vm_name = "test2"
        self.getXML()
        #vm = self.connection.lookupByName(vm_name)

        domain = Element('domain', attrib={'type':'qemu'})

        name = Element('name')
        name.text = vm_name

        uuid = Element('uuid')
        uuid.text = utils.randomUUID()

        description = Element('description')
        description.text = "test description"

        memory = Element('memory', attrib={'unit': 'KiB'})
        memory.text = "256"

        currentMemory = Element('currentMemory', attrib={'unit': 'KiB'})
        currentMemory.text = "256"
        
        vcpu = Element('vcpu', attrib={'placement': 'static'})
        vcpu.text = "1"

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
        dom = self.connection.createXML(xml, 0)
        dom = self.connection.defineXML(xml)

        
        
        
    def devices(self, boot, cdrom):
        text = """
        <devices>
        <emulator>/usr/bin/kvm</emulator>
        <disk device="disk" type="file">
        <driver name="qemu" type="raw" />
        <source file="%s" />
        <target bus="ide" dev="hda" />
        <address bus="0" controller="0" target="0" type="drive" unit="0" />
        </disk>
        <disk device="cdrom" type="file">
        <driver name="qemu" type="raw" />
        <source file="%s" />
        <target bus="ide" dev="hdb" />
        <readonly />
        <address bus="0" controller="0" target="0" type="drive" unit="1" />
        </disk>
        <controller index="0" model="ich9-ehci1" type="usb">
        <address bus="0x00" domain="0x0000" function="0x7" slot="0x06" type="pci" />
        </controller>
        <controller index="0" model="ich9-uhci1" type="usb">
        <master startport="0" />
        <address bus="0x00" domain="0x0000" function="0x0" multifunction="on" slot="0x06" type="pci" />
        </controller>
        <controller index="0" model="ich9-uhci2" type="usb">
        <master startport="2" />
        <address bus="0x00" domain="0x0000" function="0x1" slot="0x06" type="pci" />
        </controller>
        <controller index="0" model="ich9-uhci3" type="usb">
        <master startport="4" />
        <address bus="0x00" domain="0x0000" function="0x2" slot="0x06" type="pci" />
        </controller>
        <controller index="0" model="pci-root" type="pci" />
        <controller index="0" type="ide">
        <address bus="0x00" domain="0x0000" function="0x1" slot="0x01" type="pci" />
        </controller>
        <controller index="0" type="virtio-serial">
        <address bus="0x00" domain="0x0000" function="0x0" slot="0x05" type="pci" />
        </controller>
        <interface type="network">
        <mac address="52:54:00:e1:fb:d5" />
        <source network="default" />
        <model type="rtl8139" />
        <address bus="0x00" domain="0x0000" function="0x0" slot="0x03" type="pci" />
        </interface>
        <serial type="pty">
        <target port="0" />
        </serial>
        <console type="pty">
        <target port="0" type="serial" />
        </console>
        <channel type="spicevmc">
        <target name="com.redhat.spice.0" type="virtio" />
        <address bus="0" controller="0" port="1" type="virtio-serial" />
        </channel>
        <input bus="ps2" type="mouse" />
        <input bus="ps2" type="keyboard" />
        <graphics autoport="yes" type="spice">
        <image compression="off" />
        </graphics>
        <sound model="ich6">
        <address bus="0x00" domain="0x0000" function="0x0" slot="0x04" type="pci" />
        </sound>
        <video>
        <model heads="1" ram="65536" type="qxl" vgamem="16384" vram="65536" />
        <address bus="0x00" domain="0x0000" function="0x0" slot="0x02" type="pci" />
        </video>
        <redirdev bus="usb" type="spicevmc"></redirdev>
        <redirdev bus="usb" type="spicevmc"></redirdev>
        <memballoon model="virtio">
        <address bus="0x00" domain="0x0000" function="0x0" slot="0x07" type="pci" />
        </memballoon>
        </devices>
        """ % (boot, cdrom)
        
        return ET.XML(text)

