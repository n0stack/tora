# coding:UTF-8
from show.vminfo import DomainInfo
from show.storageinfo import StorageInfo
from create.vm import CreateVM
from create.storage import CreateStorage
import json

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource


app = Flask(__name__)
api = Api(app)


def abort_if_vmid_doesnt_exist(id):
    abort(404, message="{} doesn't exist".format(id))


class DomainInfoAll(Resource):
    def get(self):
        data = DomainInfo()
        return data.get_domain_info_all(), 200

        
class Domain(Resource):
    def get(self, func_name, id):
        data = DomainInfo()
        r_data = None
        if func_name == "state":
            r_data = data.get_state(id)
        elif func_name == "memory":
            r_data = data.get_max_memory(id)
        elif func_name == "CPU":
            r_data = data.get_CPU_number(id)

        if r_data is None:
            abort_if_vmid_doesnt_exist(id)
        else:
            return r_data, 200

            
api.add_resource(DomainInfoAll, '/vm')
api.add_resource(Domain, '/vm/<func_name>/<int:id>')


if __name__ == '__main__':
    app.run(debug=True)




#create_test = CreateVM()
#create_test("test2", os.getcwd()+"/img/cent2.img", os.getcwd()+"/iso/cent7-mini.iso", 524288, 1)

#test = DomainInfo()
#print(json.dumps(test.show_domain_info_all()))

#test = StorageInfo()
#print(json.dumps(test.show_storage_info_all()))

test = CreateStorage()
test("test", 500000, "/home/palloc/iso_file/")
