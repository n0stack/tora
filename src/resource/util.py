# coding:utf-8
from info.vm import DomainInfo
from info.pool import PoolInfo

from flask_restful import abort

def abort_if_vmid_doesnot_exist(name):
    dominfo = DomainInfo()
    if name not in dominfo.get_domain_list()['domain_list']:
        abort(404, message="{} does not exist".format(name))

def abort_if_vmid_exists(name):
    dominfo = DomainInfo()
    if name in dominfo.get_domain_list()['domain_list']:
        abort(404, message="{} does not exist".format(name))
