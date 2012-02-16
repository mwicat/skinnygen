'''
Created on Jun 10, 2011

@author: lebleu1
'''
import struct

class SCCPMessage:
    '''
    Sccp message
    '''

    def __init__(self,sccpMessageType):
        self.sccpmessageType = sccpMessageType
        self.reserved=0x00
    
    def __eq__(self,other):
        if (self.__class__.__name__ != other.__class__.__name__):
            return False
        return self.sccpmessageType == other.sccpmessageType

    def pack(self):
        return struct.pack("II",self.reserved,self.sccpmessageType)
    
    def unPack(self,buffer):
        self.buffer = buffer
        
    def toStr(self):
        return "SCCPMessage : " + hex(self.sccpmessageType)