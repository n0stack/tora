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
def abort_if_vmid_doesnt_exist(data, id):
    if id not in data.get_domain_list()['domain_list']:
        abort(404, message="{} doesn't exist".format(id))


class DomainInfoAll(Resource):
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
    def get(self, func_name, id):
        data = DomainInfo()

        # Check existance of id
        abort_if_vmid_doesnt_exist(data, id)

        if func_name == "state":
            r_data = data.get_state(id)
        elif func_name == "memory":
            r_data = data.get_max_memory(id)
        elif func_name == "CPU":
            r_data = data.get_CPU_number(id)
        
        return r_data, 200


class VMStatus(Resource):
    def post(self, name):
        data = VmOperation()
        try:
            json_data = request.get_json(force=True)
            print(json_data)
            operation = json_data["operation"]
        except:
            return {"message": "Illegal operation."}

        if operation == "start":
            r_data = data.start_vm(name)
        elif operation == "stop":
            r_data =  data.stop_vm(name)
        elif operation == "force_stop":
            r_data = data.force_stop_vm(name)
        else:
            return {"message": "No operation."}
        
        return r_data

            
api.add_resource(DomainInfoAll, '/instance')
api.add_resource(Domain, '/instance/<int:id>')
api.add_resource(VMStatus, '/power/<name>')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)



