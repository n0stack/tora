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
            info = pool.info()
            print('##############################')
            print('pool name: ' + pool.name())
            print('uuid: ' + pool.UUIDString())
            print('Autostart: '+str(pool.autostart()))
            print('Is active: '+str(pool.isActive()))
            print('Is persistent: '+str(pool.isPersistent()))
            print('Num volumes: '+str(pool.numOfVolumes()))
            print('Pool state: '+str(info[0]))
            print('Capacity: '+str(info[1]))
            print('Allocation: '+str(info[2]))
            print('Available: '+str(info[3]))
            volumes = pool.listVolumes()
            print(volumes)

            
        
