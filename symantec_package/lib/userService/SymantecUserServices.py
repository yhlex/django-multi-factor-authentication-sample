"""
.. module:: SymantecUserServices
    :platform: All platforms that are compatible with Python framework
    :synopsis: Module handles all VIP user services SOAP calls

.. moduleauthor:: Gabriel Morcote & Allen Huynh

"""

import string
import random       #random/string to generate random request IDs

### A class to represent the functions that Symantec User Services provides
class SymantecUserServices:
    """This class acts as a layer of abstraction to handling all user services Symantec VIP SOAP calls in Python.

        You call this class to handle anything that is related to authenticating users and credentials.

        Example:
            >>> client = Client("http://../vipuserservices-auth-1.7.wsdl", transport = HTTPSClientCertTransport('vip_certificate.crt','vip_certificate.crt'))
            >>> service = SymantecUserServices(client)
            >>> response = service.authenticateUser(<parameters here>)
            >>> print (response)

        .. NOTE::
            Reference HTTPHandler for further information on how to setup the client.

        """

    def __init__(self, client):
        """The class takes in only a SOAP client object.

            Arg:
                client (suds.client Client): The client to handle the SOAP calls

            .. NOTE::
                Any parameters that are of "None" type are optional fields.

        """
        self.client = client
        self.response = None   #most recent response in str format
        # self.onBehalfOfAccountId = onBehalfOfAccountId
        # self.iaInfo = iaInfo
        # self.includePushAttributes = includePushAttributes


    ###  Call the client's authenticateUser function
    # def authenticateUser(self, requestId, userId, securityCode, pin=None, authContext=None, onBehalfOfAccountId=None):
    #     res = self.client.service.authenticateUser(requestId=requestId,onBehalfOfAccountId=onBehalfOfAccountId,
    #                                                userId=userId, otpAuthData={"otp": securityCode},
    #                                                pin=pin, authContext=authContext)
    #     self.response = res
    #     # print(res)
    #     return res


    # I fixed this one; Someone fix the following ones
    def authenticateUser(self, requestId, userId, otp1, otp2=None, value=None, key="authLevel.level", authContext=None,
                         pin=None, onBehalfOfAccountId=None):
        if otp2 == None:
            if value != None:
                res = self.client.service.authenticateUser(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId,
                                                   userId=userId, pin=pin, otpAuthData={"otp": otp1},
                                                       authContext={"params":{"Key":key, "Value":value}})
            else:
                res = self.client.service.authenticateUser(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId,
                                                   userId=userId, pin=pin, otpAuthData={"otp": otp1},
                                                       authContext=authContext)
        else:
            if value != None:
                res = self.client.service.authenticateUser(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId,
                                                   userId=userId, pin=pin, otpAuthData={"otp": otp1, "otp2": otp2},
                                                       authContext={"params": {"Key": key, "Value": value}})
            else:
                res = self.client.service.authenticateUser(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId,
                                                   userId=userId, pin=pin, otpAuthData={"otp": otp1, "otp2": otp2},
                                                       authContext=authContext)
        self.response = res
        # print(res)
        return res


    def authenticateCredentials(self, requestId, credentials, otp1=None, otp2=None, pushAuthData=None, activate=None, authContext=None, onBehalfOfAccountId=None):
        # NOTE: otp or pushAuthData is required!
        if otp1 is None:
            res = self.client.service.authenticateCredentials(requestId=requestId, credentials=credentials, onBehalfOfAccountId=onBehalfOfAccountId,
                                                              otpAuthData=None, pushAuthData=pushAuthData, activate=activate, authContext=authContext)
        elif otp2 is not None:
            res = self.client.service.authenticateCredentials(requestId=requestId, credentials=credentials,
                                                              onBehalfOfAccountId=onBehalfOfAccountId,
                                                              otpAuthData={"otp": otp1, "otp2": otp2}, pushAuthData=None,
                                                              activate=activate, authContext=authContext)
        else:
            res = self.client.service.authenticateCredentials(requestId=requestId, credentials=credentials, onBehalfOfAccountId=onBehalfOfAccountId,
                                                          otpAuthData={"otp": otp1}, pushAuthData=pushAuthData, activate=activate, authContext=authContext)
        self.response = res
        # print(self.response)
        return res

    # Missing some parameters in Documentation!!!!!
    def authenticateCredentialWithPush(self, requestId, credentialId,activate=None, pushAuthData=None,
                                        key="authLevel.level", value=None, authContext=None, onBehalfOfAccountId=None):
        """
            :description: *Authenticates a user via a Push notification using their credential ID.*
            :note:
            :param requestId: A unique identifier of the request for the enterprise application. This may be useful for troubleshooting
            :type requestId: string
            :param activate: Activates a credential. If otpAuthData is provided, it consumes the OTP to authenticate. If pushAuthData is used, sends a push notification to the credential for authentication.
            :type activate: boolean
            :param authContext: A map containing the parameters that control how the authentication is performed. VIP User Services accepts an authentication level for the authContext field. The authentication level defines the credential types that can be validated with this request. This level must match an authentication level configured in VIP Manager. ■ Key: Enter authLevel.level ■ Value: Enter the authentication level value (as an integer from 1 - 10).
            :type authContext: string
            :param value: The user's specified gateway Account password
            :type value: string
            :returns: the return SOAP response.
            :raises:

        """
        if pushAuthData is None: # make sure we do not miss the tags for it as it is required
            pushAuthData={}
        if value is not None:
            res = self.client.service.authenticateCredentials(requestId=requestId,
                                                              onBehalfOfAccountId=onBehalfOfAccountId,
                                                              credentials={"credentialId": credentialId,
                                                                           "credentialType": "STANDARD_OTP"},
                                                              activate=activate, otpAuthData=None,
                                                              pushAuthData=pushAuthData,
                                                              authContext={"params": {"Key": key, "Value": value}})
        else:
            res = self.client.service.authenticateCredentials(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId,
                                                              credentials={"credentialId": credentialId,
                                                                           "credentialType": "STANDARD_OTP"},
                                                              activate=activate, otpAuthData=None,
                                                              pushAuthData=pushAuthData,
                                                              authContext=authContext)

        self.response = res

        return res




    def authenticateCredentialWithSMS(self, requestId, credentialId_phoneNumber, otp1,otp2=None, activate=None, onBehalfOfAccountId=None):
        if otp2 is None:
            res = self.client.service.authenticateCredentials(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId,
                                                              credentials={"credentialId": credentialId_phoneNumber,
                                                                           "credentialType": "SMS_OTP"},
                                                              activate=activate, otpAuthData={"otp": otp1})
        else:
            res = self.client.service.authenticateCredentials(requestId=requestId,
                                                              onBehalfOfAccountId=onBehalfOfAccountId,
                                                              credentials={"credentialId": credentialId_phoneNumber,
                                                                           "credentialType": "SMS_OTP"},
                                                              activate=activate, otpAuthData={"otp": otp1, "otp2": otp2})
        self.response = res
        # print(self.response)
        return res


    def authenticateCredentialWithStandard_OTP(self, requestId, credentialId,otp1,otp2=None, activate=None, onBehalfOfAccountId=None):
        if otp2 is None:
            res = self.client.service.authenticateCredentials(requestId=requestId,
                                                              onBehalfOfAccountId=onBehalfOfAccountId,
                                                              credentials={"credentialId": credentialId,
                                                                           "credentialType": "STANDARD_OTP"},
                                                              activate=activate, otpAuthData={"otp": otp1})
        else:
            res = self.client.service.authenticateCredentials(requestId=requestId,
                                                              onBehalfOfAccountId=onBehalfOfAccountId,
                                                              credentials={"credentialId": credentialId,
                                                                           "credentialType": "STANDARD_OTP"},
                                                              activate=activate, otpAuthData={"otp": otp1, "otp2": otp2})
        self.response = res
        # print(self.response)
        return res


    def authenticateUserWithPush(self, requestId, userId, pin=None, pushAuthData=None,
                                 key="authLevel.level", value=None, authContext=None, onBehalfOfAccountId=None):
        if value is None:
            res = self.client.service.authenticateUserWithPush(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId,
                                                               userId=userId, pin=pin, pushAuthData=pushAuthData,
                                                               authContext=authContext)
        else:
            res = self.client.service.authenticateUserWithPush(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId,
                                                         userId=userId, pin=pin, pushAuthData=pushAuthData,
                                                         authContext={"params":{"Key":key, "Value":value}})
        self.response = res
        # print(self.response)
        return res


    def checkOtp(self, requestId, userId, otp1, otp2=None, value=None, key="authLevel.level", authContext=None, onBehalfOfAccountId=None):
        if otp2 is None:
            if value is not None:
                res = self.client.service.authenticateUser(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId,
                                                   userId=userId, otpAuthData={"otp": otp1},
                                                       authContext={"params":{"Key":key, "Value":value}})
            else:
                res = self.client.service.authenticateUser(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId,
                                                   userId=userId, otpAuthData={"otp": otp1},
                                                       authContext=authContext)
        else:
            if value is not None:
                res = self.client.service.authenticateUser(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId,
                                                   userId=userId,  otpAuthData={"otp": otp1, "otp2": otp2},
                                                       authContext={"params": {"Key": key, "Value": value}})
            else:
                res = self.client.service.authenticateUser(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId,
                                                   userId=userId, otpAuthData={"otp": otp1, "otp2": otp2},
                                                       authContext=authContext)
        self.response = res
        # print(res)
        return res

    def confirmRisk(self, requestId, UserId, EventId, VerifyMethod=None, KeyValuePair=None, onBehalfOfAccountId=None):
        # note: keyValuePair is a list containing key + value
        res = self.client.service.confirmRisk(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId, UserId=UserId,
                                              EventId=EventId, VerifyMethod=VerifyMethod, KeyValuePair=KeyValuePair)
        self.response = res
        # print(res)
        return res

    def denyRisk(self, requestId, UserId, EventId, VerifyMethod=None, IAAuthData=None, isRememberDevice=None,
                 FriendlyName=None, KeyValuePair=None, onBehalfOfAccountId=None):
        res = self.client.service.denyRisk(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId,
                                              UserId=UserId, EventId=EventId, VerifyMethod=VerifyMethod, IAAuthData=IAAuthData,
                                              RememberDevice=isRememberDevice, FriendlyName=FriendlyName, KeyValuePair=KeyValuePair)
        self.response = res
        # print(res)
        return res

    def evaluateRisk(self, requestId, UserId, IpAddress, UserAgent, IAAuthData=None, KeyValuePair=None, onBehalfOfAccountId=None):
        res = self.client.service.evaluateRisk(requestId=requestId, onBehalfOfAccountId=onBehalfOfAccountId, UserId=UserId,
                                               Ip=IpAddress, UserAgent=UserAgent, IAAuthData=IAAuthData, KeyValuePair=KeyValuePair)
        self.response = res
        # print (res)
        return res

    def getFieldContent(self, fieldname):
        """

            :description: *Get content of items in response message*
            :note: Works only for one line item
            :param fieldname: Item name
            :type fieldname: string
            :returns: The content of input fieldname

        """
        info_list = self.__str__().split('\n')

        for item in info_list:
            if fieldname in item:
                return item.split('=')[1][1:]

        pass

    # iterates through first level of main response fields from previous SOAP call and tells what fields are accessible
    # gives warning if that field is a list containing more sub-fields
    def getPreviousResponseFirstPairs(self):
        """

            :description: *Gets the 1st level of important main response fields from previous VIP SOAP call and tells what fields are accessible*
            :note: This will not work if there was no previous call in the client.
            :returns: list -- Containing all the first pair values of each tuple

        """
        # list to hold first pair value in tuples
        firstPairs = []
        warnings = []
        index = 0
        # NOTE: SOAP response is similar to tuples and dictionaries but are not of those types.
        for tup in self.response:
            # tup[0] #first of pair (key)
            # tup[1] #second of pair (value)

            # WE check for list
            if type(tup[1]) is list:
                warning = "WARNING: '" + str(tup[0]) + "' at " + "index(" + str(index) + ") is a list!!!"
                print(warning)
                warnings.append(warning)
            firstPairs.append(str(tup[0]))
            index += 1
        return firstPairs

    # iterates through first level of main response fields and tells what fields are accessible
    # gives warning if that field is a list containing more sub-fields
    def getResponseFirstPairs(self, response):
        """

            :description: *Gets the 1st level of important main response fields from the VIP SOAP call and tells what fields are accessible*
            :note: This requires the SOAP response as a parameter.
            :param response: The SOAP response
            :type response: list of tuples
            :returns: list -- Containing all the first pair values of each tuple

        """
        # list to hold first pair value in tuples
        firstPairs = []
        warnings = []
        index = 0
        # NOTE: SOAP response is similar to tuples and dictionaries but are not of those types.
        for tup in response:
            # tup[0] #first of pair (key)
            # tup[1] #second of pair (value)

            # WE check for list
            if type(tup[1]) is list:
                warning = "WARNING: '" + str(tup[0]) + "' at " + "index(" + str(index) + ") is a list!!!"
                print (warning)
                warnings.append(warning)
            firstPairs.append(str(tup[0]))
            index += 1
        return firstPairs

    # Returns the field value at that key of the pair; this uses the previous response
    def getPreviousResponseValue(self, firstPair):
        """

            :description: *Gets the 1st level of important main response fields from the VIP SOAP call and tells what fields are accessible*
            :note: This will not work if there was no previous call in the client.
            :param firstPair: The first pair in the tuple field
            :type firstPair: string
            :returns: The field value at the pair key

        """
        return self.response[firstPair]

    # Returns the field value at that key of the pair
    def getResponseValue(self, response, firstPair):
        """

            :description: *Gets the 1st level of important main response fields from the VIP SOAP call and tells what fields are accessible*
            :note: This requires the SOAP response as a parameter.
            :param response: The SOAP response
            :type response: list of tuples
            :param firstPair: The first pair in the tuple field
            :type firstPair: string
            :returns: The field value at the pair key

        """
        return response[firstPair]
