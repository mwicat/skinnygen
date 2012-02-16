'''
Created on Jun 14, 2011

@author: lebleu1
'''
import unittest
from sccp.messagefactory import MessageFactory
from sccp.sccpregisterack import SCCPRegisterAck
from sccp.sccpcapabilitiesreq import SCCPCapabilitiesReq
from sccp.sccpkeepaliveack import SCCPKeepAliveAck
from sccp.sccpdefinetimedate import SCCPDefineTimeDate
from sccp.sccplinestat import SCCPLineStat


class TestMessageFactory(unittest.TestCase):

    def setUp(self):
        self.messageFactory = MessageFactory()

    def testCreateRegisterAck(self):
        receivedBuffer = "\x00\x00\x00\x00\x81\x00\x00\x00\x00\x0b\x00\x00"
    
        msg = self.messageFactory.create(receivedBuffer)
        
        self.assertTrue(isinstance(msg, SCCPRegisterAck))

    def testCreateCapabilitiesReq(self):
        receivedBuffer = "\x00\x00\x00\x00\x9b\x00\x00\x00\x00\x0b\x00\x00"
    
        msg = self.messageFactory.create(receivedBuffer)
        
        self.assertTrue(isinstance(msg, SCCPCapabilitiesReq))
        
    def testCreateKeepAliveAck(self):
        receivedBuffer = "\x00\x00\x00\x00\x00\x01\x00\x00\x00\x0b\x00\x00"
    
        msg = self.messageFactory.create(receivedBuffer)
        
        self.assertTrue(isinstance(msg, SCCPKeepAliveAck))

    def testCreateDefineTimeDate(self):
        receivedBuffer = "\x00\x00\x00\x00\x94\x00\x00\x00\x00\x0b\x00\x00"
    
        msg = self.messageFactory.create(receivedBuffer)
        
        self.assertTrue(isinstance(msg, SCCPDefineTimeDate))
        
    def testCreateLineStat(self):
        receivedBuffer = "\x00\x00\x00\x00\x92\x00\x00\x00\x00\x0b\x00\x00"
        msg = self.messageFactory.create(receivedBuffer)
        
        self.assertTrue(isinstance(msg, SCCPLineStat))
        

    def testCreateUnkownType(self):
        receivedBuffer = "\x00\x00\x00\x00\xFF\xFF\x00\x00\x00\x0b\x00\x00"
        msg = self.messageFactory.create(receivedBuffer)
        self.assertEquals(0xFFFF,msg.sccpmessageType)
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()