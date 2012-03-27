'''
Created on Jun 14, 2011

@author: lebleu1
'''
from sccp.sccpmessage import SCCPMessage
from sccp.sccpmessagetype import SCCPMessageType
from struct import unpack


class SCCPLineStat(SCCPMessage):
    

    def __init__(self):
        SCCPMessage.__init__(self, SCCPMessageType.LineStatMessage)
        self.line=0
        self.dirNumber = ""
        
        
    def unPack(self,buffer):
        self.line = unpack("I",buffer[:4])[0]
        self.dirNumber = buffer[4:].split("\x00")[0]

