'''
Created on Jun 14, 2011

@author: lebleu1
'''
from sccp.sccpmessage import SCCPMessage
from sccp.sccpmessagetype import SCCPMessageType
from struct import pack

class SCCPSoftKeyEvent(SCCPMessage):
    '''
    sccp register message
    '''
    
    def __init__(self,event,line=0,callId=0):
        '''
        Constructor
        '''
        SCCPMessage.__init__(self, SCCPMessageType.SoftKeyEventMessage)
        self.event=event
        self.line=line
        self.callId=callId
        
    def __eq__(self,other):
        if (self.event != other.event):
            return False
        if (self.line != other.line):
            return False
        if (self.callId != other.callId):
            return False
        return SCCPMessage.__eq__(self, other)
        
    def pack(self):
        strPack = SCCPMessage.pack(self)
        strPack = strPack + pack("I",self.event)
        strPack = strPack + pack("I",self.line)
        strPack = strPack + pack("I",self.callId)
        return strPack
