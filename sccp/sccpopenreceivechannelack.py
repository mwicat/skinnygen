'''
Created on Jun 14, 2011

@author: lebleu1
'''
from sccp.sccpmessage import SCCPMessage
from sccp.sccpmessagetype import SCCPMessageType

from struct import pack
from network.ipAddress import IpAddress


class SCCPOpenReceiveChannelAck(SCCPMessage):
    

    def __init__(self, channelStatus, ipAddress, portNumber, passThruPartyId):
        SCCPMessage.__init__(self, SCCPMessageType.OpenReceiveChannelAck)
        self.channelStatus = channelStatus
        self.ipAddress = IpAddress(ipAddress)
        self.portNumber = portNumber
        self.passThruPartyId = passThruPartyId

    def pack(self):
        strPack = SCCPMessage.pack(self)
        strPack = strPack + pack("I",self.channelStatus)
        strPack = strPack + self.ipAddress.pack()
        strPack = strPack + pack("I",self.portNumber)
        strPack = strPack + pack("I",self.passThruPartyId)
        return strPack
        


