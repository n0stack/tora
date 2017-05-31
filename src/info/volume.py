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
        self.pool = self.connection.storagePoolLookupByName(poolname)

        # failed
        if self.pool is None:
            return {"message": "Failed."}, 400

        volumes = []

        for volume in self.pool.listVolumes():
            voltmp = {}
            volumes.update({"name": volume})

            volinfo = self.pool.storageVolLookupByName(volume).info()
            voltmp.update({"type": str(volinfo[0])})
            voltmp.update({"capacity": str(volinfo[1])})
            voltmp.update({"allocation": str(volinfo[2])})

            volumes.append(voltmp)

        return {"volumes": volumes}
            
