# coding:UTF-8
from showinfo.vminfo import DomainInfo
from create.vm import CreateVM
import json

create_test = CreateVM()
create_test("test12", "/koko.img", "/wei.iso", 40)

#test = DomainInfo()
#print(json.dumps(test.show_domain_info_all()))

