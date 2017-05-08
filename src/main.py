# coding:UTF-8
from ShowInfo.vm_info import DomainInfo
import json

test = DomainInfo()
print(json.dumps(test.show_domain_info_all()))
