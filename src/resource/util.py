# coding:utf-8
from info.vm import DomainInfo
from info.pool import PoolInfo

from flask_restful import abort

def abort_if_vmname_exists(name):
    dominfo = DomainInfo()
    if dominfo.vmname_exists(name) is True:
        abort(409, message="{} exists".format(name))
    else:
        pass

def abort_if_vmname_doesnot_exist(name):
    dominfo = DomainInfo()
    if dominfo.vmname_exists(name) is True:
        pass
    else:
        abort(404, message="{} does not exist".format(name))        

def abort_if_poolname_exists(name):
    poolinfo = PoolInfo()
    if poolinfo.poolname_exists(name) is True:
        abort(409, message="{} exists".format(name))
    else:
        pass
        
def abort_if_poolname_doesnot_exist(name):
    poolinfo = PoolInfo()
    if poolinfo.poolname_exists(name) is True:
        pass
    else:
        abort(404, message="{} does not exist".format(name))        
