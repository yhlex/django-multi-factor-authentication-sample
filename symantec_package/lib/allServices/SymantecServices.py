
class SymantecServices:

    import sys
    #sys.path.append("/home/oem/PycharmProjects/Securitas_Dev/Securitas") # remove this when finish

    from symantec_package.lib.userService.SymantecUserServices import SymantecUserServices
    from symantec_package.lib.queryService.SymantecQueryServices import SymantecQueryServices
    from symantec_package.lib.managementService.SymantecManagementServices import SymantecManagementServices

    def __init__(self, queryClient, managementClient, userClient):

        queryService = self.SymantecQueryServices(queryClient)
        managementService = self.SymantecManagementServices(managementClient)
        userService = self.SymantecUserServices(userClient)
        self.queryService = queryService
        self.managementService = managementService
        self.userService = userService
        self.queryClient = queryClient
        self.managementClient = managementClient
        self.userClient = userClient
        self.response  = None


# ******************** MULTIPLE CLIENT FUNCTIONS
    def authenticateUserWithPushThenPolling(self, requestIdPush, requestIdPoll, userId, queryTimeout=60, queryInterval=5,
                                            displayParams=None, requestParams=None, authContext=None, onBehalfOfAccountId=None):
        import time

        res = ""

        push = self.userService.authenticateUserWithPush(requestIdPush, userId)
        print (push)
        transaction_id = self.userService.getFieldContent('transactionId').strip('"')
        isExit = False
        isError = False

        for sec in range(1,queryTimeout // queryInterval):
            if isExit:
                break
            time.sleep(queryInterval) # NEED NEW SOLUTION for querying on interval in python

            #if sec % queryInterval == 0:
            poll_status = str(self.queryClient.service.pollPushStatus(requestId=requestIdPoll,
                                                                           onBehalfOfAccountId=onBehalfOfAccountId,
                                                                           transactionId=transaction_id))
            res = poll_status
            #now check response for status
            lines = poll_status.split('\n')
            for line in lines:
                if isError:
                    errorMessage = line.split('=')[1][1:].strip('\n')
                    print("\n\tError: " + errorMessage)
                    isExit = True
                    break
                if "status " in line:
                    status = line.split('=')[1][1:].strip('\n')
                    #res = status
                    if "0000" in status: # ignore this first status for polling connection
                        continue
                    elif "7000" in status:
                        print("\nSUCCESS! Push Accepted!")
                        isExit = True
                        break
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
        return(str(res))

# ******************** QUERY
    def getUserInfo(self, requestId, userId, onBehalfOfAccountId=None, iaInfo=True, includePushAttributes=True):
        res = self.queryService.getUserInfo(requestId, userId, onBehalfOfAccountId , iaInfo , includePushAttributes )
        self.response = res
        print(self.response)
        return str(res)

    def pollPushStatus(self, requestId, transactionId):
        res = self.queryService.pollPushStatus( requestId,  transactionId)
        self.response = res
        print(self.response)
        return str(res)

    def getCredentialInfo(self, requestId, credentialId, credentialType="STANDARD_OTP",
                          includePushAttributes=None, onBehalfOfAccountId=None):
        res = self.queryService.getCredentialInfo(requestId, credentialId, credentialType,
                          includePushAttributes , onBehalfOfAccountId )
        self.response = res
        print(self.response)
        return str(res)

    def getServerTime(self, requestId, onBehalfOfAccountId=None):
        res = self.queryService.getServerTime(requestId, onBehalfOfAccountId)
        self.response = res
        print(self.response)
        return str(res)

    def getTemporaryPasswordAttributes(self, requestId, userId, onBehalfOfAccountId=None):
        res = self.queryService.getTemporaryPasswordAttributes(requestId, userId, onBehalfOfAccountId)
        self.response = res
        print(self.response)
        return str(res)

# ******************** MANAGEMENT
    def sendOtpSMS(self, requestId, userId, phoneNumber, isGatewayAcctInfo=False, onBehalfOfAccountId=None,
                   smsFrom=None, messageTemplate=None, gatewayId=None, gatewayPassword=None ):
        res = self.managementService.sendOtp(requestId, userId, phoneNumber, isGatewayAcctInfo, onBehalfOfAccountId,
                   smsFrom , messageTemplate, gatewayId, gatewayPassword )

        pass

    # simple create user function. check for tests LOOK AND WRITE SOME TOO if you think needed
    def createUser(self, requestId, userId, onBehalfOfAccountId=None, pin=None, forcePinChange=None):
        res = self.managementService.createUser(requestId, userId, onBehalfOfAccountId , pin , forcePinChange )
        return str(res)

    #simple delete user function
    def deleteUser(self, requestId, userId, onBehalfOfAccountId=None):
        res = self.managementService.deleteUser(requestId, userId, onBehalfOfAccountId )
        return str(res)

# ********************USER SERVICE
    def authenticateUser(self, requestId, userId, pin=None, otp=None, authContext=None):
        self.userService.authenticateUser( requestId,  userId,  pin, otp, authContext)
        pass


    def authenticateCredentials(self, requestId, credentials, otpAuthData=None, pushAuthData=None, activate=None):
        self.userService.authenticateCredentials( requestId,  credentials, otpAuthData, pushAuthData, activate)
        pass

    #SMS
    def authenticateWithSMS(self, requestId, credentialId_phoneNumber, securityCode, activate=None):
        self.userService.authenticateCredentials(requestId, credentialId_phoneNumber, securityCode, activate )

        pass
    #Normal 6 digit
    def authenticateWithStandard_OTP(self, requestId, credentialId, securityCode, activate=None):
        self.userService.authenticateCredentials(requestId, credentialId, securityCode, activate)

        pass

    ###  Call the client's authenticateUserWithPush function
    def authenticateUserWithPush(self, requestId, userId, pin=None, displayParams=None, requestParams=None, authContext=None):
        self.userService.authenticateUserWithPush(requestId, userId, pin, displayParams , requestParams , authContext )
        #print(self.response)
        pass


    def getFieldContent(self, fieldname):
        info_list = self.response.split('\n')
        for item in info_list:
            if fieldname in item:
                return item.split('=')[1][1:]
