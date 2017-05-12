# coding:UTF-8
from showinfo.vminfo import DomainInfo
from showinfo.storageinfo import StorageInfo
from create.vm import CreateVM
import json
import os

#create_test = CreateVM()
#create_test("test2", os.getcwd()+"/img/cent2.img", os.getcwd()+"/iso/cent7-mini.iso", 524288, 1)

#test = DomainInfo()
#print(json.dumps(test.show_domain_info_all()))

test = StorageInfo()
test.show_storage_info_all()
