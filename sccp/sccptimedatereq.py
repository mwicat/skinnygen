'''
Created on Jun 14, 2011

@author: lebleu1
'''
from sccp.sccpmessage import SCCPMessage
from sccp.sccpmessagetype import SCCPMessageType


class SCCPTimeDateReq(SCCPMessage):
    

    def __init__(self):
        SCCPMessage.__init__(self, SCCPMessageType.TimeDateReqMessage)
        


