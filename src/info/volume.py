#coding: UTF-8
import sys
import libvirt
from xml.dom import minidom
from kvmconnect.base import BaseReadOnly

class VolumeInfo(BaseReadOnly):
    """
    Show Volume's information
    """
    def __init__(self):
        super().__init__()

    def get_volume_list(self, poolname):
        volumes = self.connection.storagePoolLookupByName(poolname)

        # failed
        if volumes is None:
            return {"message": "Failed."}, 400

        return {"volumes": vomules.listVolumes()}
            
            
