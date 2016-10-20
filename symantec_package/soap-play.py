import urllib.request, http.client, socket
from suds.client import Client
from suds.transport.http import HttpTransport, Reply, TransportError

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
sys.path.append("/Users/hanlinye/Documents/banking-app-example/")
from symantec_package.lib.userService.SymantecUserServices import SymantecUserServices
from symantec_package.lib.queryService.SymantecQueryServices import SymantecQueryServices
logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)

from suds.client import Client
#from suds.transport.https import


# the URLs for now which will have the WSDL files and the XSD file
url = 'http://webdev.cse.msu.edu/~yehanlin/vip/vipuserservices-query-1.7.wsdl'
userservices_url = 'http://webdev.cse.msu.edu/~morcoteg/Symantec/WSDL/vipuserservices-auth-1.4.wsdl'

# initializing the Suds clients for each url, with the client certificate youll have in the same dir as this file
query_services_client = Client(url,
         transport = HTTPSClientCertTransport('vip_certificate.crt','vip_certificate.crt'))
user_services_client = Client(userservices_url,
         transport = HTTPSClientCertTransport('vip_certificate.crt','vip_certificate.crt'))


#get_user_info_result = client.service.getUserInfo(requestId="123123", userId="y1196293")

# Gabe here, testing pushing to phone with wrapper class SymantecUserServices
#test_user_services_object = SymantecUserServices(user_services_client)
#send_push_to_phone_result = test_user_services_object.authenticateUserWithPush("push_123", "y1196293")
#print(test_user_services_object.authenticateUserWithPushAndPoll(client,"12312312","y1196293"))

test_user_services_object = SymantecUserServices(user_services_client)
test_query_services_object = SymantecQueryServices(query_services_client)
#test_management_services_object = SymantecManagementServices(management_client)

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

#authenticateUserWithPushThenPolling(user_services_client, query_services_client, "Push_Test", "PushPollTest","Arren_phone")

# Authenticate with push, and wait for response (NOTE: this should go into a class that handles all the Services
def authenticateUserWithPushThenPolling(user_client, query_client, requestIdPush, requestIdPoll, userId, queryTimeout=60, queryInterval=5,
                                        displayParams=None, requestParams=None, authContext=None, onBehalfOfAccountId=None):
    import time
    user_service = SymantecUserServices(user_services_client)
    query_service = SymantecQueryServices(query_client)

    push = user_service.authenticateUserWithPush(requestIdPush, userId)
    print (push)
    print(user_service)
    transaction_id = user_service.getFieldContent('transactionId').strip('"')
    print(transaction_id)
    isExit = False
    isError = False

    for sec in range(1,queryTimeout // queryInterval):
        if isExit:
            break
        time.sleep(queryInterval) # NEED NEW SOLUTION for querying on interval in python

        #if sec % queryInterval == 0:
        poll_status = str(query_client.service.pollPushStatus(requestId=requestIdPoll,
                                                                       onBehalfOfAccountId=onBehalfOfAccountId,
                                                                       transactionId=transaction_id))
        #now check response for status
        lines = poll_status.split('\n')
        for line in lines:
            if isError:
                errorMessage = line.split('=')[1][1:].strip('\n')
                print("\n\tError: " + errorMessage)
                isExit = True
                return 0
            if "status " in line:
                status = line.split('=')[1][1:].strip('\n')
                if "0000" in status: # ignore this first status for polling connection
                    continue
                elif "7000" in status:
                    print("\nSUCCESS! Push Accepted!")
                    isExit = True
                    #break
                    return 1
                elif "7001" in status:
                    print("\nIN PROGRESS...")
                    break
                elif "7002" in status:
                    print("\nPush Denied!")
                    isExit = True
                    break
                else:
                    #print("\n\tError status!")  # should later have it print status message
                    isError = True


authenticateUserWithPushThenPolling(user_services_client, query_services_client, "Push_Test", "PushPollTest","Arren_phone")

