# coding:UTF-8
from showinfo.vminfo import DomainInfo
from create.vm import CreateVM
import json

create_test = CreateVM()
create_test("test2", "/koko.img", "/wei.iso", 256, 1)

#test = DomainInfo()
#print(json.dumps(test.show_domain_info_all()))

