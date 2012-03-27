'''
Created on Jun 14, 2011

@author: lebleu1
'''
from sccp.sccpmessage import SCCPMessage
from sccp.sccpmessagetype import SCCPMessageType
from struct import unpack


class SCCPRegisterAck(SCCPMessage):
    

    def __init__(self):
        SCCPMessage.__init__(self, SCCPMessageType.RegisterAckMessage)
        self.keepAliveInterval = 50
        self.dateTemplate = ""
        self.secondaryKeepAliveInterval=32
        
        
    def unPack(self,buffer):
        self.keepAliveInterval = unpack("I",buffer[:4])[0]
        self.dateTemplate = buffer[4:].split("\x00")[0]
        endDateTemplate =  buffer[4:].find("\x00")
        
        bufferLeft = buffer[4+endDateTemplate+3:]
        self.secondaryKeepAliveInterval = unpack("I",bufferLeft[:4])[0]


