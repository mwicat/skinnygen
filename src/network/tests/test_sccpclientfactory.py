'''
Created on Jun 14, 2011

@author: lebleu1
'''
import unittest
from network.sccpclientfactory import SCCPClientFactory
from sccp.sccpmessagetype import SCCPMessageType
from sccp.sccpregisterack import SCCPRegisterAck
from sccp.sccpmessage import SCCPMessage
from tests.mock import Mock



class TestSCCPClientFactory(unittest.TestCase):
    handled = False
    
    def setUp(self):
        self.handled = False
        self.unkown = False
        self.lastMessageTypeReceived = 0x0000
        self.clientFactory = SCCPClientFactory(self.unused, self.unused) 

    def unused(self):
        '''
        unused callback
        '''
    def handleUnknown(self,message):
        self.lastMessageTypeReceived = message.sccpmessageType
        self.unkown = True
    
    def handleMessage(self,message):
        self.lastMessageTypeReceived = message.sccpmessageType
        self.handled = True
        

    def testHandleMessage(self):
        self.clientFactory = SCCPClientFactory(self.unused, self.unused) 
        self.clientFactory.addHandler(SCCPMessageType.RegisterAckMessage, self.handleMessage)
        self.clientFactory.handleMessage(SCCPRegisterAck())
        self.assertTrue(self.handled)
        self.assertEquals(SCCPMessageType.RegisterAckMessage,self.lastMessageTypeReceived)
        
    def testHandleUnknownMessage(self):
        message = SCCPMessage(0xFFFF)
        self.clientFactory.handleUnknownMessage(self.handleUnknown)
        self.clientFactory.handleMessage(message)
        self.assertTrue(self.unkown)
        self.assertEquals(0xFFFF,self.lastMessageTypeReceived)
        
    
    def testSendSccpMessage(self):
        message = SCCPMessage(SCCPMessageType.ButtonTemplateReqMessage)
        networkClient = Mock()
        self.clientFactory.client=networkClient
        self.clientFactory.sendSccpMessage(message)
        networkClient.sendString.assert_called_with(message.pack())
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
