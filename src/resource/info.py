# coding:utf-8
from info.vm import DomainInfo
from resource.util import abort_if_vmid_doesnot_exist

from flask_restful import Resource, reqparse


class DomainAll(Resource):
    """
    This api will return all domain's information
    """
    def get(self):
        dominfo = DomainInfo()
        return dominfo.get_domain_info_all(), 200


class Domain(Resource):
    """
    get domain info
    """
    def get(self, name):
        dominfo = DomainInfo()

        # check vm name
        abort_if_vmid_doesnot_exist(name)
        r_data = dominfo.get_domain_info(name)

        return r_data, 200
