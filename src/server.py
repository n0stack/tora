# coding:UTF-8
from show.vminfo import DomainInfo
from show.storageinfo import StorageInfo
from create.vm import CreateVM
from create.storage import CreateStorage
from operation.vm import VmOperation
import json

from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource


app = Flask(__name__)
api = Api(app)

# Check 404
def abort_if_vmid_doesnt_exist(name):
    data = DomainInfo()
    if name not in data.get_domain_list()['domain_list']:
        abort(404, message="{} doesn't exist".format(name))


class DomainAll(Resource):
    """
    This api will return all domain's information
    """
    def get(self):
        data = DomainInfo()
        return data.get_domain_info_all(), 200

        
class Domain(Resource):
    """
    about vm operation
    """
    def get(self, name):
        data = DomainInfo()

        # Check existance of name
        abort_if_vmid_doesnt_exist(name)
        r_data = data.get_domain_info(name)

        return r_data, 200


class VMStatus(Resource):
    """
    Operate vm's power.
    """
    def post(self, name):
        data = VmOperation()

        # Check existance of name
        abort_if_vmid_doesnt_exist(name)

        # If post data is illegal
        try:
            post_data = json.loads(request.data.decode('utf-8'))
            operation = post_data["operation"]
        except:
            return {"message": "Illegal operation."}, 400

        # Operate VM
        if operation == "start":
            r_data, status_code = data.start_vm(name)
        elif operation == "stop":
            r_data, status_code =  data.force_stop_vm(name)
        else:
            return {"message": "Bad operation."}, 400
        
        return r_data, status_code

            
api.add_resource(DomainAll, '/instance')
api.add_resource(Domain, '/instance/<name>')
api.add_resource(VMStatus, '/power/<name>')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)



