# coding:utf-8
import operation.vm as VMop
from info.vm import DomainInfo
from resource.util import abort_if_vmid_doesnot_exist

from flask_restful import Resource, reqparse


class VM(Resource):
    """
    check/change VM status
    """
    def get(self):
        """
        get all vm info
        """
        dominfo = DomainInfo()
        return dominfo.get_domain_info_all(), 200


class VMname(Resource):
    def get(self, name):
        """
        get vm info
        """
        dominfo = DomainInfo()

        # check vm name
        abort_if_vmid_doesnot_exist(name)
        r_data = dominfo.get_domain_info(name)

        return r_data, 200

    def post(self, name):
        """
        create vm 
        """
        pass

    def put(self, name):
        """
        change vm status
        """
        # check vm name
        abort_if_vmid_doesnot_exist(name)

        status = VMop.Status()

        # set parser
        parser = reqparse.RequestParser()
        parser.add_argument('operation', type=str, location='json', required=True)

        args = parser.parse_args()
        operation = args['operation']

        # manage VM
        try:
            r_data, status_code = {
                "start": status.start,
                "stop": status.stop,
            }[operation](name)
        except KeyError:
            return {"message": "invalid operation"}, 400

        return r_data, status_code

    def delete(self, name):
        """
        delete vm
        """
        # check vm name
        abort_if_vmid_doesnot_exist(name)

        vmdelete = VMop.Delete()
        return vmdelete(name)
