'''
Created on Jun 14, 2011

@author: lebleu1
'''
from sccp.sccpmessage import SCCPMessage
from sccp.sccpmessagetype import SCCPMessageType
from struct import unpack


class SCCPOpenReceiveChannel(SCCPMessage):    

    def __init__(self):
        SCCPMessage.__init__(self, SCCPMessageType.OpenReceiveChannel)
        self.echoCancelType = 0
        self.bitRate = 0

        
    def unPack(self,buffer):
        datas = unpack("IIIIII",buffer[:24])
        self.conferenceId = datas[0]
        self.passThruPartyId =datas[1]
        self.msPacket =datas[2]
        self.payloadCapability =datas[3]
        self.echoCancelType =datas[4]
        self.bitRate =datas[5]
