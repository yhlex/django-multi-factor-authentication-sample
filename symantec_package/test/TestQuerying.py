import unittest
from suds.client import Client
import sys
sys.path.append("/home/oem/PycharmProjects/Securitas_Dev/Securitas") # remove this when finish, allen's path
# from symantec_package.lib.userService.SymantecUserServices import SymantecUserServices
from symantec_package.lib.queryService.SymantecQueryServices import SymantecQueryServices
# from symantec_package.lib.managementService.SymantecManagementServices import SymantecManagementServices
# from symantec_package.lib.allServices.SymantecServices import SymantecServices
from symantec_package.HTTPHandler import setConnection, HTTPSClientAuthHandler, HTTPSClientCertTransport

class TestQuerying(unittest.TestCase):
    def setUp(self):
        # the URLs for now which will have the WSDL files and the XSD file
        query_services_url = 'http://webdev.cse.msu.edu/~yehanlin/vip/vipuserservices-query-1.7.wsdl'
        # userservices_url = 'http://webdev.cse.msu.edu/~morcoteg/Symantec/WSDL/vipuserservices-auth-1.4.wsdl'
        # managementservices_url = 'http://webdev.cse.msu.edu/~huynhall/vipuserservices-mgmt-1.7.wsdl'

        # initializing the Suds clients for each url, with the client certificate youll have in the same dir as this file
        query_services_client = Client(query_services_url,
                                       transport=HTTPSClientCertTransport('vip_certificate.crt', 'vip_certificate.crt'))
        # user_services_client = Client(userservices_url,
        #                               transport=HTTPSClientCertTransport('vip_certificate.crt', 'vip_certificate.crt'))
        # management_client = Client(managementservices_url,
        #                            transport=HTTPSClientCertTransport('vip_certificate.crt', 'vip_certificate.crt'))

        # get_user_info_result = query_services_client.service.getUserInfo(requestId="123123", userId="y1196293")

        # test_user_services_object = SymantecUserServices(user_services_client)
        self.test_query_services = SymantecQueryServices(query_services_client)
        # test_management_services_object = SymantecManagementServices(management_client)
        # self.test_services = SymantecServices(query_services_client, management_client, user_services_client)


    def test_getUserInfo(self):
        result = self.test_query_services.getUserInfo("TEST", "Arren_phone")
        self.assertTrue("0000" in str(result))  # check if success status
        self.assertTrue('userId = "Arren_phone"')
        pass

    def test_ServerTime(self):
        result = self.test_query_services.getServerTime("TEST")
        self.assertTrue("0000" in str(result))

        pass

    def test_temp_pass(self):
        result = self.test_query_services.getTemporaryPasswordAttributes("temp_pass", "Arren_phone")

        self.assertTrue("6017" in str(result)) # not set

        pass

    def test_poll(self):
        result = self.test_query_services.pollPushStatus("TEST_POLL", "123321")

        self.assertTrue("7005" in str(result)) # should not exist
        self.assertTrue("0000" in str(result))
        pass

    def test_credentialInfo(self):
        result = self.test_query_services.getCredentialInfo("cred123test", "VSTZ43724471")

        self.assertTrue("VSTZ43724471" in str(result))
        self.assertTrue("STANDARD_OTP" in str(result))
        self.assertTrue("0000" in str(result))
        pass

if __name__ == '__main__':
    unittest.main()