

class SymantecQueryServices:

    def __init__(self, client):
        self.client = client
        self.response = None    #the most recent response

    def getUserInfo(self, requestId, userId, onBehalfOfAccountId=None, iaInfo=True, includePushAttributes=True):
        res = self.client.service.getUserInfo(requestId=requestId, userId=userId,
                                        onBehalfOfAccountId=onBehalfOfAccountId, iaInfo=iaInfo,
                                        includePushAttributes=includePushAttributes)
        return str(res)

    def pollPushStatus(self, requestId, transactionId, onBehalfOfAccountId=None):
        res = self.client.service.pollPushStatus(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId,transactionId=transactionId)
        self.response = res
        print(self.response)
        return str(res)

    def getCredentialInfo(self, requestId, credentialId, credentialType="STANDARD_OTP",
                          includePushAttributes=None, onBehalfOfAccountId=None):
        res = self.client.service.getCredentialInfo(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId,credentialId=credentialId,
                                                    credentialType=credentialType, includePushAttributes=includePushAttributes)
        self.response = res
        print(self.response)
        return str(res)

    def getServerTime(self, requestId, onBehalfOfAccountId=None):
        res = self.client.service.getServerTime(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId)
        self.response = res
        print(self.response)
        return str(res)

    def getTemporaryPasswordAttributes(self, requestId, userId, onBehalfOfAccountId=None):
        res = self.client.service.getTemporaryPasswordAttributes(requestId=requestId,
                                                                                  onBehalfOfAccountId=onBehalfOfAccountId,
                                                                                  userId=userId)
        self.response = res
        print(self.response)
        return str(res)

    def getFieldContent(self, fieldname):
        info_list = self.__str__().split('\n')

        for item in info_list:
            if fieldname in item:
                return item.split('=')[1][1:]

        pass
