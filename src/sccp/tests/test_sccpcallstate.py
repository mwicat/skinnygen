'''
@author: lebleu1
'''
import unittest
from sccp.sccpcallstate import SCCPCallState


class TestSccpCallState(unittest.TestCase):


    def testUnPack(self):
        callState = SCCPCallState()
        receivedBuffer = '\x04\x00\x00\x00\x01\x00\x00\x00\x1a\x00'\
                        '\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00'
        callState.unPack(receivedBuffer)
        self.assertEquals(callState.callState,SCCPCallState.SCCP_CHANNELSTATE_RINGING)
        self.assertEquals(callState.line,1)
        self.assertEquals(callState.callId,26)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()