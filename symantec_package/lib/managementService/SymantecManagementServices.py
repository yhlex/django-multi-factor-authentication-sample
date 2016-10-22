
class SymantecManagementServices:
    def __init__(self, client):
        self.client = client
        self.response = None

    def sendOtpSMS(self, requestId, userId, phoneNumber, isGatewayAcctInfo=False, onBehalfOfAccountId=None,
                   smsFrom=None, messageTemplate=None, gatewayId=None, gatewayPassword=None ):
        if isGatewayAcctInfo:
            res = self.client.service.sendOtp(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId,userId=userId,
                                        smsDeliveryInfo={"phoneNumber": phoneNumber, "smsFrom": smsFrom,
                                        "messageTemplate":messageTemplate,
                                                         "gatewayAcctInfo":{"Id":gatewayId, "Password":gatewayPassword}})
        else:
            res = self.client.service.sendOtp(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId, userId=userId,
                                        smsDeliveryInfo={"phoneNumber": phoneNumber, "smsFrom": smsFrom,
                                                         "messageTemplate": messageTemplate})
        self.response = str(res)
        print(self.response)
        pass

    # simple create user function. check for tests LOOK AND WRITE SOME TOO if you think needed
    def createUser(self, requestId, userId, onBehalfOfAccountId=None, pin=None, forcePinChange=None):
        res = self.client.service.createUser(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId, \
                                             userId=userId, pin=pin, forcePinChange=forcePinChange)
        print(str(res))
        return str(res)

    #simple delete user function
    def deleteUser(self, requestId, userId, onBehalfOfAccountId=None):
        res = self.client.service.deleteUser(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId, \
                                             userId=userId)
        print(str(res))
        return str(res)
    