'''
@author: lebleu1
'''
import unittest
from sccp.sccpstarttone import SCCPStartTone


class TestSccpStartTone(unittest.TestCase):


    def testUnPack(self):
        startTone = SCCPStartTone()
        receivedBuffer ='\x25\x00\x00\x00\x0F\x00\x00\x00\x01\x00\x00\x00\x1a\x00\x00\x00'
        startTone.unPack(receivedBuffer)
        self.assertEquals(startTone.tone,37)
        self.assertEquals(startTone.toneTimeout,15)
        self.assertEquals(startTone.line,1)
        self.assertEquals(startTone.callId,26)
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()