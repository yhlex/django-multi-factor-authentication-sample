class SymantecQueryServices:

    def __init__(self, client):
        self.client = client
        self.response = None    #the most recent response

    def getUserInfo(self, requestId, userId, onBehalfOfAccountId=None, iaInfo=True, includePushAttributes=True):
        res = self.client.service.getUserInfo(requestId=requestId, userId=userId,
                                        onBehalfOfAccountId=onBehalfOfAccountId, iaInfo=iaInfo,
                                        includePushAttributes=includePushAttributes)
        return str(res)

    def pollPushStatus(self, requestId, transactionId):
        res = self.client.service.pollPushStatus(requestId=requestId, transactionId=transactionId)
        self.response = res
        print(self.response)
        #push_res = clients.service.pollPushStatus(requestId='13498345', transactionId=transactionId)
        # if ("approved" in str(push_res)):
	    #    return HttpResponse("Succeed")
        pass


    def getFieldContent(self, fieldname):
        info_list = self.__str__().split('\n')

        for item in info_list:
            if fieldname in item:
                return item.split('=')[1][1:]

        pass