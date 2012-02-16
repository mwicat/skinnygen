'''
Created on Jun 14, 2011

@author: lebleu1
'''
import unittest
from sccp.sccpregisterack import SCCPRegisterAck


class TestSccpRegisterAck(unittest.TestCase):


    def testUnPack(self):
        registerAck = SCCPRegisterAck()
        receivedBuffer = "\x0b\x00\x00\x00\x44\x2e\x4d\x2e\x59\x00\x00\x00\x14\x00\x00\x00\x0b\x20\xf1\xff"
        registerAck.unPack(receivedBuffer)
        self.assertEquals(registerAck.keepAliveInterval,11)
        self.assertEquals(registerAck.dateTemplate,"D.M.Y")
        self.assertEquals(registerAck.secondaryKeepAliveInterval,20)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()