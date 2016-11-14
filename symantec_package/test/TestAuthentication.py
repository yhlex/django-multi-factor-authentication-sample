import unittest
from suds.client import Client
from symantec_package.lib.userService.SymantecUserServices import SymantecUserServices
from symantec_package.HTTPHandler import setConnection, HTTPSClientAuthHandler, HTTPSClientCertTransport

class TestAuthentication(unittest.TestCase):
    def setUp(self):
        # the URLs for now which will have the WSDL files and the XSD file
        query_services_url = 'http://webdev.cse.msu.edu/~yehanlin/vip/vipuserservices-query-1.7.wsdl'
        userservices_url = 'http://webdev.cse.msu.edu/~morcoteg/Symantec/WSDL/vipuserservices-auth-1.7.wsdl'

        # initializing the Suds clients for each url, with the client certificate youll have in the same dir as this file
        query_services_client = Client(query_services_url,
                                       transport=HTTPSClientCertTransport('vip_certificate.crt', 'vip_certificate.crt'))
        user_services_client = Client(userservices_url,
                                      transport=HTTPSClientCertTransport('vip_certificate.crt', 'vip_certificate.crt'))

        self.test_user_services_object = SymantecUserServices(user_services_client)

    def test_OTP(self):
        authenticate_result = self.test_user_services_object.authenticateUser("test_otp", \
                                                                    "gabe_phone", "991483")
        self.assertTrue("0000" in str(authenticate_result))
        pass

    def test_authenticateCredWithOTP(self):
        authenticate_result = self.test_user_services_object.authenticateCredentialWithStandard_OTP("test_cred_otp", "VSMT16833399",
                                                                                                    "374125")

        self.assertTrue("0000" in str(authenticate_result))
        pass

    def test_authenticateCredWithOTP_activate(self):
        authenticate_result_activate = self.test_user_services_object.authenticateCredentialWithStandard_OTP(
            "test_cred_otp", "VSMT16833399",
            "374125", True)
        self.assertTrue("0000" in str(authenticate_result_activate))
        pass

    def test_push(self):
        authenticate_result = self.test_user_services_object.authenticateCredentialWithPush("push_456", "VSMT16833399",
                                                                                       "Use my Push!")
        print(str(authenticate_result))
        self.assertTrue("6040" in str(authenticate_result))
        pass


if __name__ == '__main__':
    unittest.main()