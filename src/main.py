# coding:UTF-8
from showinfo.vminfo import DomainInfo
import json

test = DomainInfo()
print(json.dumps(test.show_domain_info_all()))
