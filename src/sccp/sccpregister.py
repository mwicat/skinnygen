'''
Created on Jun 14, 2011

@author: lebleu1
'''
from sccp.sccpmessage import SCCPMessage
from sccp.sccpmessagetype import SCCPMessageType
from struct import pack
from network.ipAddress import IpAddress

class SCCPRegister(SCCPMessage):
    '''
    sccp register message
    '''
    TelecasterBus=0x08
    MAXSTREAMS=0
    STATION_INSTANCE=1
    STATION_USERID=0
    

    def __init__(self,deviceName,ipAddress):
        '''
        Constructor
        '''
        SCCPMessage.__init__(self, SCCPMessageType.RegisterMessage)
        self.deviceName=deviceName
        self.ipAddress = IpAddress(ipAddress)
        self.stationUserId=self.STATION_USERID
        self.stationInstance=self.STATION_INSTANCE
        self.deviceType=self.TelecasterBus
        self.maxStreams=self.MAXSTREAMS
        
    def __eq__(self,obj):
        if (self.deviceName != obj.deviceName):
            return False
        if (self.ipAddress != obj.ipAddress):
            return False
        return True
        
        
    def pack(self):
        strPack = SCCPMessage.pack(self) + self.deviceName + "\x00"
        strPack = strPack + pack("II",self.stationUserId,self.stationInstance)
        strPack = strPack + self.ipAddress.pack()
        strPack = strPack + pack("III",self.deviceType,self.maxStreams,0)
        strPack = strPack + '\x0B'+ '\x00'+ '\x60'+ '\x85'
        strPack = strPack + pack('IIII',0,0,0,0)
        return strPack