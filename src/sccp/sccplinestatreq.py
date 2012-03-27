'''
Created on Jun 14, 2011

@author: lebleu1
'''
from sccp.sccpmessage import SCCPMessage
from sccp.sccpmessagetype import SCCPMessageType
from struct import pack


class SCCPLineStatReq(SCCPMessage):
    

    def __init__(self,line):
        SCCPMessage.__init__(self, SCCPMessageType.LineStatReqMessage)
        self.line = line
        


    def pack(self):
        strPack = SCCPMessage.pack(self)
        strPack = strPack + pack("L",self.line)
        return strPack

