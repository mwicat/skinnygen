'''
Created on Jun 14, 2011

@author: lebleu1
'''
from sccp.sccpmessage import SCCPMessage
from sccp.sccpmessagetype import SCCPMessageType
from struct import unpack


class SCCPSetRinger(SCCPMessage):    

    def __init__(self):
        SCCPMessage.__init__(self, SCCPMessageType.SetRingerMessage)
        
    def unPack(self,buffer):
        datas = unpack("IIII",buffer[:16])
        self.ringType = datas[0]
        self.ringMode =datas[1]
        self.line =datas[2]
        self.callId =datas[3]
