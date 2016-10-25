import string
import random       #random/string to generate random request IDs

### A class to represent the functions that Symantec User Services provides

# authenticateUserWithPush -- sends a Push to a user's phone
class SymantecUserServices:

    # we should have a helper function to randomly generate request ID's

    # for now, pass in the client and play with it. pass in other things like requestID and such to
    #      this class's member functions since those aren't static. The client MAY be static, so thats for now
    def __init__(self, client, onBehalfOfAccountId=None, iaInfo=True, includePushAttributes=True):
        self.client = client
        self.response = None   #most recent response in str format
        self.onBehalfOfAccountId = onBehalfOfAccountId
        self.iaInfo = iaInfo
        self.includePushAttributes = includePushAttributes


    # def __str__(self, requestId, userId):
    #     res = str(self.client.service.authenticateUserWithPush(requestId=requestId, userId=userId))
    #     return res

    ###  Call the client's authenticateUser function
    def authenticateUser(self, requestId, userId, securityCode, pin=None, authContext=None):
        res = self.client.service.authenticateUser(requestId=requestId, userId=userId, otpAuthData={"otp": securityCode},
                                                   pin=pin, authContext=authContext)
        self.response = str(res)
        print(str(res))
        return str(res)


    def authenticateCredentials(self, requestId, credentials, otpAuthData=None, pushAuthData=None, activate=None):
        res = self.client.service.authenticateCredentials(requestId=requestId, credentials=credentials, otpAuthData=otpAuthData)
        self.response = str(res)
        # print(self.response)
        return str(res)

    #SMS
    def authenticateWithSMS(self, requestId, credentialId_phoneNumber, securityCode, activate=None):
        res = self.client.service.authenticateCredentials(requestId=requestId, activate=activate,
                                                          credentials={"credentialId": credentialId_phoneNumber,
                                                                       "credentialType": "SMS_OTP"},
                                                          otpAuthData={"otp": securityCode})
        self.response = str(res)
         # print(self.response)
        return str(res)
    #Normal 6 digit
    def authenticateWithStandard_OTP(self, requestId, credentialId, securityCode, activate=None):
        res = self.client.service.authenticateCredentials(requestId=requestId, activate= activate,
                                                          credentials={"credentialId": credentialId,
                                                                       "credentialType": "STANDARD_OTP"},
                                                          otpAuthData={"otp": securityCode})
        self.response = str(res)
        # print(self.response)
        return str(res)

    ###  Call the client's authenticateUserWithPush function
    def authenticateUserWithPush(self, requestId, userId, pin=None, displayParams=None, requestParams=None, authContext=None):
        res = self.client.service.authenticateUserWithPush(requestId=requestId, userId=userId)
        self.response = str(res)
        # print(self.response)
        return str(res)


    def getFieldContent(self, fieldname):
        info_list = self.response.split('\n')
        for item in info_list:
            if fieldname in item:
                return item.split('=')[1][1:]
