'''
Created on Jun 14, 2011

@author: lebleu1
'''
from sccp.sccpmessage import SCCPMessage
from sccp.sccpmessagetype import SCCPMessageType
from struct import pack

class SCCPRegisterAvailableLines(SCCPMessage):
    '''
    sccp register message
    '''
    def __init__(self):
        '''
        Constructor
        '''
        SCCPMessage.__init__(self, SCCPMessageType.RegisterAvailableLinesMessage)
        self.nboflines=1
        
    def pack(self):
        strPack = SCCPMessage.pack(self)
        strPack = strPack + pack("L",self.nboflines)
        return strPack
