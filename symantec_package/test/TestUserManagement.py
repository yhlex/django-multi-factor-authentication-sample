import unittest
from suds.client import Client
import sys
sys.path.append("/home/oem/PycharmProjects/Securitas_Dev/Securitas")

from symantec_package.lib.managementService.SymantecManagementServices import SymantecManagementServices
from symantec_package.HTTPHandler import setConnection, HTTPSClientAuthHandler, HTTPSClientCertTransport

class TestUserManagement(unittest.TestCase):
    def setUp(self):
        # the URLs for now which will have the WSDL files and the XSD file
        query_services_url = 'http://webdev.cse.msu.edu/~yehanlin/vip/vipuserservices-query-1.7.wsdl'
        userservices_url = 'http://webdev.cse.msu.edu/~morcoteg/Symantec/WSDL/vipuserservices-auth-1.4.wsdl'
        managementservices_url = 'http://webdev.cse.msu.edu/~huynhall/vipuserservices-mgmt-1.7.wsdl'

        # initializing the Suds clients for each url, with the client certificate youll have in the same dir as this file
        management_client = Client(managementservices_url,
                                   transport=HTTPSClientCertTransport('vip_certificate.crt', 'vip_certificate.crt'))

        self.test_management_services_object = SymantecManagementServices(management_client)

    def test_create_user(self):
        user = self.test_management_services_object.createUser("new_user456", "new_user2")
        self.assertTrue("0000" in str(user))

        user2 = self.test_management_services_object.createUser("new_user456", "new_user2")
        self.assertTrue("6002" in str(user2))
        pass

    def test_delete_user(self):
        user = self.test_management_services_object.deleteUser("delete_user123", "new_user2")
        self.assertTrue("0000" in str(user))

        user2 = self.test_management_services_object.deleteUser("delete_user456", "new_user2")
        self.assertTrue("6003" in str(user2))
        pass


if __name__ == '__main__':
    unittest.main()