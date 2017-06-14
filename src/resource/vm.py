# coding:utf-8
import operation.vm as VMop
from info.vm import DomainInfo
from resource.util import abort_if_vmname_doesnot_exist, abort_if_vmname_exists

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

{
    "cpu": {
        "arch": "cpu architecutre (ex. x86_64, ...)",
        "nvcpu": "number of vcpus",
    },
    "memory": "memory size of VM",
    "disk": {
        "pool": "pool name where disk is stored",
        "size": "volume size"
    },
    "cdrom": "iso image path",
    "mac_addr": "mac address (automatically generated if not specfied)",
    "vnc_password": "vnc password (no password if not specified)"
}
        """
        # check vm name
        abort_if_vmname_exists(name)

        # set parser
        parser = reqparse.RequestParser()
        parser.add_argument('cpu', type=dict, location='json', required=True)
        parser.add_argument('memory', type=str, location='json', required=True)
        parser.add_argument('disk', type=dict, location='json', required=True)
        parser.add_argument('cdrom', type=str, location='json', required=True)
        parser.add_argument('mac_addr', type=str, location='json', 
                required=False, default=None)
        parser.add_argument('vnc_password', type=str, location='json', 
                required=False, default="")

        args = parser.parse_args()
        _args = (name, args['cpu'], args['memory'], args['disk'], 
                args['cdrom'], args['mac_addr'], args['vnc_password'])

        vmcreate = VMop.Create()
        result = vmcreate(*_args)

        if result is False:
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
            result = {
                "start": status.start,
                "stop": status.stop,
                "force_stop": status.force_stop
            }[operation](name)
        except KeyError:
            return {"message": "invalid operation"}, 400

        if result is False:
            return {"message": "failed"}, 409
        return {"message": "successful"}, 200

    def delete(self, name):
        """
        delete vm
        """
        # check vm name
        abort_if_vmname_doesnot_exist(name)

        vmdelete = VMop.Delete()
        result = vmdelete(name)

        if result is False:
            return {"message":"failed"}, 400
        return {"message": "success"}, 200

    
class VMclone(Resource):
    """
    clone VM

{
    "name": "new vm name",
    "vnc_password": "vnc passoword of new vm"
}
    """
    def post(self, name):
        # check vm name
        abort_if_vmname_doesnot_exist(name)

        # set parser
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, location='json', required=True)
        parser.add_argument('vnc_password', type=str, location='json', 
                required=False, default='')

        args = parser.parse_args()
        dst = args['name']
        vncpass = args['vnc_password']

        # check vm name
        abort_if_vmname_exists(dst)

        vmclone = VMop.Clone()
        result = vmclone(name, dst, vncpass)

        if result is False:
            return {'message': 'failed'}, 400
        return {'message': 'successful'}, 201, {'Location': '/vm/{}'.format(dst)}
