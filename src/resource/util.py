# coding:utf-8
from info.vm import DomainInfo
from info.pool import PoolInfo

from flask_restful import abort

def abort_if_vmname_exists(name):
    dominfo = DomainInfo()
    try:
        dominfo.connection.lookupByName(name)
        abort(409, message="{} exists".format(name))
    except:
        pass

def abort_if_vmname_doesnot_exist(name):
    dominfo = DomainInfo()
    try:
        dominfo.connection.lookupByName(name)
    except:
        abort(404, message="{} does not exist".format(name))        

def abort_if_poolname_exists(name):
    poolinfo = PoolInfo()
    try:
        poolinfo.connection.lookupByName(name)
        abort(409, message="{} exists".format(name))
    except:
        pass
        
def abort_if_poolname_doesnot_exist(name):
    try:
        poolinfo.connection.lookupByName(name)
    except:
        abort(404, message="{} does not exist".format(name))        
