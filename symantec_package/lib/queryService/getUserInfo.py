# import logging
# <<<<<<< Updated upstream
#
# #logging.basicConfig(level=logging.INFO)
# #logging.getLogger('suds.client').setLevel(logging.DEBUG)
#
# class getUserInfo:
#
#     def __init__(self,client, requestId, userId, onBehalfOfAccountId=None, iaInfo=True, includePushAttributes=True):
# =======
# logging.basicConfig(level=logging.INFO)
# logging.getLogger('suds.client').setLevel(logging.DEBUG)
#
#
# class getUserInfo:
#
#     def __init__(self,client, requestId, userId, onBehalfOfAccountId=None,iaInfo=True, includePushAttributes=True):
# >>>>>>> Stashed changes
#         self.client = client
#         self.requestId = requestId
#         self.userId = userId
#         self.onBehalfOfAccountId = onBehalfOfAccountId
#         self.iaInfo = iaInfo
#         self.includePushAttributes = includePushAttributes
#
#
#     def __str__(self):
# <<<<<<< Updated upstream
#         res = str(self.client.service.getUserInfo(requestId=self.requestId, userId=self.userId,
#                                    onBehalfOfAccountId=self.onBehalfOfAccountId, iaInfo=self.iaInfo,
#                                    includePushAttributes=self.includePushAttributes))
#         return res
#
#     def getFieldContent(self,fieldname):
#         info_list = self.__str__().split('\n')
#
#         for item in info_list:
#             if fieldname in item:
#
#                 return item.split('=')[1][1:]
# =======
#         return \
#             str(self.client.service.getUserInfo(requestId=self.requestId, userId=self.userId,
#                                    onBehalfOfAccountId=self.onBehalfOfAccountId, iaInfo=self.iaInfo,
#                                    includePushAttributes=self.includePushAttributes))
#
#     def getCredentialId(self):
#         info_list = self.__str__().split('\n')
#         for item in info_list:
#             if 'CredentialId' in item:
#                 return item.split('=')[1]
#
# >>>>>>> Stashed changes
