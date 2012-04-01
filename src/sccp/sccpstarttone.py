'''
Created on Jun 17, 2011

@author: lebleu1
'''
from sccp.sccpmessage import SCCPMessage
from sccp.sccpmessagetype import SCCPMessageType
from struct import unpack

class SCCPStartTone(SCCPMessage):

    SCCP_TONE_INSIDE = 0x21
    SCCP_TONE_ALERTING = 0x24
    SCCP_TONE_BUSY = 0x30

    def __init__(self):
        SCCPMessage.__init__(self, SCCPMessageType.StartToneMessage)
                
    def unPack(self, buffer):
        datas = unpack('IIII',buffer[0:16])
        self.tone = datas[0]
        self.toneTimeout=datas[1]
        self.line=datas[2]
        self.callId=datas[3]
