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
    def get_storage_info_all(self):
        storage = []

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

            storage.append(pool_info)

        return storage
