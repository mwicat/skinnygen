'''
Created on Jun 10, 2011

@author: lebleu1
'''
import unittest
from sccp.sccpmessage import SCCPMessage
from sccp.sccpmessagetype import SCCPMessageType


class Test(unittest.TestCase):

    

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testPack(self):
        message = SCCPMessage(SCCPMessageType.RegisterMessage)
        self.assertEquals("\x00\x00\x00\x00\x01\x00\x00\x00",message.pack())
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()