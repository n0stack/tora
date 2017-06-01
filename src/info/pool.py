# coding: UTF-8
import libvirt
from xml.dom import minidom
from kvmconnect.base import BaseReadOnly

class PoolInfo(BaseReadOnly):
    """
    Show Storage Pool's information
    """

    def __init__(self):
        super().__init__()

    # Show storage pool's information
    def get_pool_info_all(self):
        storage_pool = []

        pools = self.connection.listAllStoragePools(0)

        for pool in pools:
            pool_info = {}
            info = pool.info()
            pool_info.update({'name': pool.name()})
            pool_info.update({'uuid': pool.UUIDString()})
            pool_info.update({'Autostart': pool.autostart()})
            pool_info.update({'state': info[0]})
            pool_info.update({'capacity': info[1]})
            pool_info.update({'allocation': info[2]})
            pool_info.update({'available': info[3]})
            pool_info.update({'is_active': pool.isActive()})
            pool_info.update({'is_persistent': pool.isPersistent()})
            pool_info.update({'volumes': pool.listVolumes()})

            storage_pool.append(pool_info)

        return {"pools": storage_pool}

    def get_pool_info(self, name):
        pool = self.connection.storagePoolLookupByName(name)
        info = pool.info()
        pool_info = {}
        
        pool_info.update({'name': pool.name()})
        pool_info.update({'name': pool.UUIDString()})
        pool_info.update({'name': pool.autostart()})
        pool_info.update({'name': info[0]()})
        pool_info.update({'name': info[1]()})
        pool_info.update({'name': info[2]()})
        pool_info.update({'name': info[3]()})
        pool_info.update({'name': pool.isActive()})
        pool_info.update({'name': pool.isPersistent()})
        pool_info.update({'name': pool.listVolumes()})

        return pool_info
        
    def poolname_exists(self, name):
        try:
            self.connection.storagePoolLookupByName(name)
        except:
            return False
        return True
    
            
        
