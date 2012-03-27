'''
Created on Jun 14, 2011

@author: lebleu1
'''
from sccp.sccpmessage import SCCPMessage
from sccp.sccpmessagetype import SCCPMessageType
from struct import pack
from network.ipAddress import IpAddress

class SCCPCapabilitiesRes(SCCPMessage):
    '''
    sccp register message
    '''
    def __init__(self):
        '''
        Constructor
        '''
        SCCPMessage.__init__(self, SCCPMessageType.CapabilitiesResMessage)
        self.capCount=3
        self.payLoads="\x19\x00\x00\x00\x78\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        self.payLoads=self.payLoads+"\x04\x00\x00\x00\x28\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        self.payLoads=self.payLoads+"\x02\x00\x00\x00\x28\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        
    def pack(self):
        strPack = SCCPMessage.pack(self)
        strPack = strPack + pack("L",self.capCount)
        strPack = strPack + self.payLoads
        return strPack
