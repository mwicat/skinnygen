'''
@author: lebleu1
'''
import unittest
from sccp.sccpsoftkeyevent import SCCPSoftKeyEvent


class TestSccpSoftKeyEvent(unittest.TestCase):


    def testPack(self):
        softKeyEvent = SCCPSoftKeyEvent(9,1,54)
        bufferToSend ='\x00\x00\x00\x00\x26\x00\x00\x00\x09\x00\x00\x00\x01\x00\x00\x00\x36\x00\x00\x00'
        self.assertEquals(softKeyEvent.pack(),bufferToSend)
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()