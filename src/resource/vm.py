# coding:utf-8
import operation.vm as VMop
from resource.util import abort_if_vmid_doesnot_exist

from flask_restful import Resource, reqparse


class Status(Resource):
    """
    check/change VM status
    """
    def get(self):
        # TODO: return vm status
        pass

    def post(self):
        status = VMop.Status()

        # set parser
        parser = reqparse.RequestParser()
        parser.add_argument('operation', type=str, location='json', required=True)
        parser.add_argument('name', type=str, location='json', required=True)

        args = parser.parse_args()
        operation = args['operation']
        name = args['name']

        # check vm name
        abort_if_vmid_doesnot_exist(name)

        # manage VM
        try:
            r_data, status_code = {
                "start": status.start,
                "stop": status.stop,
            }[operation](name)
        except KeyError:
            return {"message": "invalid operation"}, 400

        return r_data, status_code


class Create(Resource):
    """
    create vm
    """
    def post(self):
        pass


class Delete(Resource):
    """
    delete vm
    """
    def post(self):
        pass
