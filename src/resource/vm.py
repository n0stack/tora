# coding:utf-8
import json
import operation.vm as VMop
from resource.util import abort_if_vmid_doesnot_exist

from flask_restful import Resource


class Status(Resource):
    """
    check/change VM status
    """
    def get(self):
        pass

    def post(self):
        status = VMop.Status()

        # check post data
        try:
            post_data = json.loads(requesst.data.decode('utf-8'))
            operation = post_data['operation']
        except:
            return {"message": "invalid operation"}, 400

        # check name
        pass


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
