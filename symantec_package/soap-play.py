import urllib.request, http.client, socket
from suds.client import Client
from suds.transport.http import HttpTransport, Reply, TransportError
import suds
from suds.sudsobject import asdict

from suds.sudsobject import asdict
import json
from datetime import datetime
def recursive_asdict(d):
    """Convert Suds object into serializable format."""
    out = {}
    for k, v in asdict(d).items():
        if type(v) is datetime:
            v = str(v)
        if hasattr(v, '__keylist__'):
            out[k] = recursive_asdict(v)
        elif isinstance(v, list):
            out[k] = []
            for item in v:
                if hasattr(item, '__keylist__'):
                    out[k].append(recursive_asdict(item))
                else:
                    out[k].append(item)
        else:
            out[k] = v
    return out

def suds_to_json(data):
    return json.dumps(recursive_asdict(data))

class HTTPSClientAuthHandler(urllib.request.HTTPSHandler):
    def __init__(self, key, cert):
        urllib.request.HTTPSHandler.__init__(self)
        self.key = key
        self.cert = cert

    def https_open(self, req):
        #Rather than pass in a reference to a connection class, we pass in
        # a reference to a function which, for all intents and purposes,
        # will behave as a constructor
        return self.do_open(self.getConnection, req)

    def getConnection(self, host, timeout=300):
        return http.client.HTTPSConnection(host,
                                       key_file=self.key,
                                       cert_file=self.cert)

class HTTPSClientCertTransport(HttpTransport):
    def __init__(self, key, cert, *args, **kwargs):
        HttpTransport.__init__(self, *args, **kwargs)
        self.key = key
        self.cert = cert

    def u2open(self, u2request):
        """
        Open a connection.
        @param u2request: A urllib2 request.
        @type u2request: urllib2.Requet.
        @return: The opened file-like urllib2 object.
        @rtype: fp
        """
        tm = self.options.timeout
        url = urllib.request.build_opener(HTTPSClientAuthHandler(self.key, self.cert))
        if self.u2ver() < 2.6:
            socket.setdefaulttimeout(tm)
            return url.open(u2request)
        else:
            return url.open(u2request, timeout=tm)



import logging
import sys
sys.path.append("/home/oem/PycharmProjects/Securitas_Dev/Securitas")
from symantec_package.lib.userService.SymantecUserServices import SymantecUserServices
from symantec_package.lib.queryService.SymantecQueryServices import SymantecQueryServices
from symantec_package.lib.managementService.SymantecManagementServices import SymantecManagementServices
from symantec_package.lib.allServices.SymantecServices import SymantecServices

logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)

from suds.client import Client
#from suds.transport.https import


# the URLs for now which will have the WSDL files and the XSD file
query_services_url = 'http://webdev.cse.msu.edu/~yehanlin/vip/vipuserservices-query-1.7.wsdl'
userservices_url = 'http://webdev.cse.msu.edu/~morcoteg/Symantec/WSDL/vipuserservices-auth-1.4.wsdl'
managementservices_url = 'http://webdev.cse.msu.edu/~huynhall/vipuserservices-mgmt-1.7.wsdl'

# initializing the Suds clients for each url, with the client certificate youll have in the same dir as this file
query_services_client = Client(query_services_url,
         transport = HTTPSClientCertTransport('vip_certificate.crt','vip_certificate.crt'))
user_services_client = Client(userservices_url,
         transport = HTTPSClientCertTransport('vip_certificate.crt','vip_certificate.crt'))
management_client = Client(managementservices_url,
         transport = HTTPSClientCertTransport('vip_certificate.crt','vip_certificate.crt'))

#get_user_info_result = query_services_client.service.getUserInfo(requestId="123123", userId="y1196293")

test_user_services_object = SymantecUserServices(user_services_client)
test_query_services_object = SymantecQueryServices(query_services_client)
test_management_services_object = SymantecManagementServices(management_client)
test_services = SymantecServices(query_services_client, management_client, user_services_client)

#send_push_to_phone_result = test_user_services_object.authenticateUserWithPush("push_123", "gabe_phone")
#print(test_user_services_object.__str__("push_123", "gabe_phone"))

#print(user_services_client)
# authenticate_result = test_user_services_object.authenticateCredentials("push_456", \
#                                                                         {"credentialId": "VSTZ39646177", "credentialType": "STANDARD_OTP"}, \
#                                                                         {"otp": "263881"})
#a_result = test_user_services_object.authenticateWithStandard_OTP("push_123", "VSTZ39646177", input("\nEnter 6-digit security code: "))
#transaction_id = test_user_services_object.getFieldContent('transactionId')
#polling = test_query_services_object.pollPushStatus("push_456", transaction_id)
#print(test_user_services_object.__str__("push_456", "gabe_phone"))



#print(str(get_user_info_result).split('\n'))

#*****************************ALLEN TESTS

### SMS test
# user_id = input("\nEnter User ID: ")
# phoneNumber = input("Enter phone number: ")
# send_SMS = test_management_services_object.sendOtpSMS("SMS_Test", user_id, phoneNumber)
# print (send_SMS)
#
# results_SMS = test_user_services_object.authenticateWithSMS("SMS_Result_Test", phoneNumber, input("\nEnter Security Code: "))
# print (results_SMS)


# testy = test_query_services_object.getUserInfo("Test12", "Arren_phone")
# tupleFirsts = test_query_services_object.getPreviousResponseFirstPairs()
# for value in tupleFirsts:
#     txt = "[1st Pair: " + value + ", \n\t2nd Pair: " + str(test_query_services_object.getPreviousResponseValue(value)) + "]"
#     if (value == "credentialBindingDetail"):
#         break
#     print (txt)

# print((testy))
# print(testy['credentialBindingDetail'])
# print(testy['credentialBindingDetail'][1]['credentialId'])
# for tup in testy:
#     print(tup)
#     print(tup[0])
#     print(tup[1])
#     print(type(tup[1]))

# testTime = test_query_services_object.getServerTime("timers")
# print (testTime)
# response_json = recursive_asdict(testTime)
# print(response_json)
# print(response_json["status"])

# response = test_user_services_object.authenticateCredentialWithPush("push_123", "VSMT16833399", True)
# response_push = recursive_asdict(response)
# print(response_push)
# print(response_push["status"])
# print (type(testTime))

# response = test_management_services_object.createUser("create_123", "new_user3")
# response_create = recursive_asdict(response)
# print(response_create)
# print(response_create["status"])

# response = test_management_services_object.deleteUser("delete_123", "test_user1")
# response_delete = recursive_asdict(response)
# print(response_delete)
# print(response_delete["status"])

# response = test_management_services_object.addCredentialOtp("add_otp_cred", "new_user3", "VSMT16833399", "STANDARD_OTP", \
#                                                                             "203472")
# response_add = recursive_asdict(response)
# print(response_add)
# print(response_add["status"])

response = test_management_services_object.removeCredential("remove_123", "new_user3", "VSMT16833399", "STANDARD_OTP")
response_del = recursive_asdict(response)
print(response_del)
print(response_del["status"])


# # test new encompassing class
#services_push = test_services.authenticateUserWithPush("push_123", "Arren_phone")
# test_services.authenticateUserWithPushThenPolling( "Push_Test", "PushPollTest","Arren_phone")

# credentialPush = test_user_services_object.authenticateCredentialWithPush("pushy123", "VSTZ43724471")
# print (credentialPush)

# d = dict(http='127.0.0.1:8080')
# query_services_client.set_options(proxy=d)
# queryClient = suds.client.Client(query_services_url)
# d = dict(http='127.0.0.1:8080')
# queryClient.set_options(proxy=d)
# print(queryClient)
# print (query_services_client)
# testObject = query_services_client.factory.create('ns0:RequestIdType')
# print(testObject)
# testObject['requestId']
# testObject="testy123"
# print(testObject)
# testy = query_services_client.service.getServerTime(testObject)
# print(testy)
#
# print(type(testy))

# t = test_query_services_object.getCredentialInfo("getCredit123","VSTZ43724471")
# print(t)
# test = [{"requestId":"getCredit123"}, {"credentialId":"VSTZ"}]
# for i in test:
#     print(i)
#     print(i["requestId"])
#     break

reply = \
"""
          <GetCredentialInfoResponse xmlns="https://schemas.symantec.com/vip/2011/04/vipuserservices">
             <requestId>getCredentialInfo123</requestId>
             <status>0000</status>
             <statusMessage>Success</statusMessage>
             <credentialId>VSTZ00001337</credentialId>
             <credentialType>STANDARD_OTP</credentialType>
             <credentialStatus>ENABLED</credentialStatus>
             <numBindings>1</numBindings>
             <userBindingDetail>
                <userId>test_phone</userId>
                <userStatus>ACTIVE</userStatus>
                <bindingDetail>
                   <bindStatus>ENABLED</bindStatus>
                   <lastBindTime>2016-09-28T00:42:54.489Z</lastBindTime>
                   <lastAuthnTime>2016-10-30T06:46:25.236Z</lastAuthnTime>
                   <lastAuthnId>38A333E53F17B1D6</lastAuthnId>
                </bindingDetail>
             </userBindingDetail>
          </GetCredentialInfoResponse>

"""
# import xmltodict
# s = xmltodict.parse(reply)
# print (s.keys())
# print(s['GetCredentialInfoResponse'])

from xml.dom.minidom import parseString
# dom = parseString(reply)
# nodes = dom.getElementsByTagName('status')
# print (nodes[0].firstChild.nodeValue)

def getElementFromTagName(xml, tag, selected=1):
    nodes = parseString(xml).getElementsByTagName(tag)
    if len(nodes) <= 0:
        return ("FAILED to retrieve any elements of the tag: " + str(tag))

    if selected < 1: # make sure no lower then first tag that appears
        selected = 1
    return nodes[selected - 1].firstChild.nodeValue

# print(getElementFromTagName(reply,"st"))