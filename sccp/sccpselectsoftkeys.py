'''
Created on Jun 17, 2011

@author: lebleu1
'''
from sccp.sccpmessage import SCCPMessage
from sccp.sccpmessagetype import SCCPMessageType
from struct import unpack

class SCCPSelectSoftKeys(SCCPMessage):

    def __init__(self):
        print '^^^^^ got soft keys'
        SCCPMessage.__init__(self, SCCPMessageType.SelectSoftKeysMessage)
        
        
    def unPack(self, buffer):
        datas = unpack('IIII',buffer[0:16])
        self.line=datas[0]
        self.callId=datas[1]
        self.softKeySet = datas[2]
        self.softKeyMap = datas[3]
