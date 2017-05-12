# coding: UTF-8
import libvirt
from xml.dom import minidom
from kvmconnect.base import BaseReadOnly


class StorageInfo(BaseReadOnly):
    """
    Show Storage Pool's information
    """

    def __init__(self):
        super().__init__()

    # Show storage pool's information
    def show_storage_info_all(self):
        storage = []
        
        pools = self.connection.listAllStoragePools(0)

        for pool in pools:

            volumes = pool.listVolumes()
            print('storage pool:' + pool.name())
            for volume in volumes:
                print('storage vol:' + volume)
        
