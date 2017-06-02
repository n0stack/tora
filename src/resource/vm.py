# coding:utf-8
import operation.vm as VMop
from info.vm import DomainInfo
from resource.util import abort_if_vmname_doesnot_exist

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
        abort_if_vmname_doesnot_exist(name)
        r_data = dominfo.get_domain_info(name)

        return r_data, 200

    def post(self, name):
        """
        create vm 
        """
        # check vm name
        abort_if_vmname_exists(name)

        status = VMop.Status()

        # set parser
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, location='json', required=True)
        parser.add_argument('boot', type=str, location='json', required=True)
        parser.add_argument('cdrom', type=str, location='json', required=True)
        parser.add_argument('memory_size', type=str, location='json', required=True)
        parser.add_argument('vcpu_num', type=str, location='json', required=True)

        args = parser.parse_args()
        _args = (args['name'], args['boot'], args['cdrom'], args['memory_size'], args['vcpu_num'])

        vmcreate = VMop.Create()
        is_success = vmcreate(*_args)

        if is_success is False:
            return {"message": "failed"}, 422
        return {"message": "successful"}, 201

    def put(self, name):
        """
        change vm status
        """
        # check vm name
        abort_if_vmname_doesnot_exist(name)

        status = VMop.Status()

        # set parser
        parser = reqparse.RequestParser()
        parser.add_argument('operation', type=str, location='json', required=True)

        args = parser.parse_args()
        operation = args['operation']

        # manage VM
        try:
            is_success = {
                "start": status.start,
                "stop": status.stop,
                "force_stop": status.force_stop
            }[operation](name)
        except KeyError:
            return {"message": "invalid operation"}, 400

        if is_success is False:
            return {"message": "failed"}, 409
        return {"message": "successful"}, 200

    def delete(self, name):
        """
        delete vm
        """
        # check vm name
        abort_if_vmname_doesnot_exist(name)

        vmdelete = VMop.Delete()
        return vmdelete(name)
