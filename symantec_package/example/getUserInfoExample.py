import logging
import sys
#logging.basicConfig(level=logging.INFO)
#logging.getLogger('suds.client').setLevel(logging.DEBUG)
from symantec_package.lib.queryService.SymantecQueryServices import SymantecQueryServices
from symantec_package import HTTPHandler

url = 'http://webdev.cse.msu.edu/~yehanlin/vip/vipuserservices-query-1.7.wsdl'

client = HTTPHandler.setConnection(url)

user = SymantecQueryServices(client)
print(user)
print('\n\n')
print('Credential Id = ' + user.getFieldContent('credentialId'))
print('Friendly Name = ' + user.getFieldContent('friendlyName'))
print('User Creation Time = ' + user.getFieldContent('userCreationTime'))
print('Last Auth Id = ' + user.getFieldContent('lastAuthnId'))

print(user.getFieldContent('isPinSet'))