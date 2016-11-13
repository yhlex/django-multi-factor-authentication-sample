import unittest
from suds.client import Client
import sys
sys.path.append("/home/oem/PycharmProjects/Securitas_Dev/Securitas")
from symantec_package.lib.userService.SymantecUserServices import SymantecUserServices
from symantec_package.HTTPHandler import setConnection, HTTPSClientAuthHandler, HTTPSClientCertTransport
from symantec_package.lib.managementService.SymantecManagementServices import SymantecManagementServices
from symantec_package.lib.queryService.SymantecQueryServices import SymantecQueryServices

class TestAuthentication(unittest.TestCase):
    def setUp(self):
        # the URLs for now which will have the WSDL files and the XSD file
        query_services_url = 'http://webdev.cse.msu.edu/~yehanlin/vip/vipuserservices-query-1.7.wsdl'
        userservices_url = 'http://webdev.cse.msu.edu/~morcoteg/Symantec/WSDL/vipuserservices-auth-1.4.wsdl'
        managementservices_url = 'http://webdev.cse.msu.edu/~huynhall/vipuserservices-mgmt-1.7.wsdl'

        # initializing the Suds clients for each url, with the client certificate youll have in the same dir as this file
        query_services_client = Client(query_services_url,
                                       transport=HTTPSClientCertTransport('vip_certificate.crt', 'vip_certificate.crt'))
        user_services_client = Client(userservices_url,
                                      transport=HTTPSClientCertTransport('vip_certificate.crt', 'vip_certificate.crt'))
        management_client = Client(managementservices_url,
                                   transport=HTTPSClientCertTransport('vip_certificate.crt', 'vip_certificate.crt'))

        self.test_user_services_object = SymantecUserServices(user_services_client)
        self.test_management_services_object = SymantecManagementServices(management_client)
        self.test_query_services_object = SymantecQueryServices(query_services_client)

    def test_OTP(self):
        authenticate_result = self.test_user_services_object.authenticateUser("push_456", \
                                                                    "gabe_phone", \
                                                                        {"otp": "734645"})
        self.assertTrue("0000" in str(authenticate_result))
        pass

    def test_push(self):
        pass


if __name__ == '__main__':
    unittest.main()