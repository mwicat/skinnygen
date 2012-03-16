'''
Created on Jun 14, 2011

@author: lebleu1
'''
from sccp.sccpmessage import SCCPMessage
from sccp.sccpmessagetype import SCCPMessageType
from struct import unpack


class SCCPDisplayPromptStatus(SCCPMessage):    

    def __init__(self):
        SCCPMessage.__init__(self, SCCPMessageType.DisplayPromptStatusMessage)

        
    def unPack(self,buffer):
        datas = unpack("I32sII",buffer[:44])
        self.messageTimeout = datas[0]
        self.displayMessage =datas[1].rstrip('\0')
        self.line =datas[2]
        self.callId =datas[3]
