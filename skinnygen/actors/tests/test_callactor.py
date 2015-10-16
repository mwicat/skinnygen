'''
Created on Jun 28, 2011

@author: lebleu1
'''
import unittest
from actors.callactor import CallActor
from tests.mock import Mock, ANY
from sccp.sccpcallstate import SCCPCallState


class Test(unittest.TestCase):
    
    
    def setUp(self):
        self.callActor = CallActor()
        self.sccpPhone = Mock()
        self.callActor.setPhone(self.sccpPhone)
        self.timerProvider = Mock()
        self.callActor.setTimerProvider(self.timerProvider)
        self.callActor.setAutoAnswer(True)

        
    def testOnCallRinging(self):
        self.callActor.handleCall(1,34,SCCPCallState.SCCP_CHANNELSTATE_RINGING)
        self.callActor.handleCall(1,34,SCCPCallState.SCCP_CHANNELSTATE_OFFHOOK)
        self.sccpPhone.answerCall.assert_called_once_with()
        
    
    def testSecondCallRinging(self):
        self.callActor.handleCall(1,34,SCCPCallState.SCCP_CHANNELSTATE_RINGING)
        self.callActor.handleCall(1,38,SCCPCallState.SCCP_CHANNELSTATE_RINGING)
        self.sccpPhone.answerCall.assert_called_once_with()

    
    def testOtherCallRingingAndGointOffHook(self):
        self.callActor.handleCall(1,34,SCCPCallState.SCCP_CHANNELSTATE_RINGING)
        self.callActor.handleCall(1,38,SCCPCallState.SCCP_CHANNELSTATE_RINGING)
        self.callActor.handleCall(1,38,SCCPCallState.SCCP_CHANNELSTATE_ONHOOK)
        self.callActor.handleCall(1,40,SCCPCallState.SCCP_CHANNELSTATE_RINGING)
        self.sccpPhone.answerCall.assert_called_once_with()
        
    
    def testOnCallEstablished(self):
        
        self.callActor.handleCall(1,34,SCCPCallState.SCCP_CHANNELSTATE_CONNECTED)
        
        
        self.timerProvider.createOneShotTimer.assert_called_with(ANY,ANY)
        
        
    def testOnCallEndTimer(self):
        self.callActor.handleCall(7,34,SCCPCallState.SCCP_CHANNELSTATE_RINGING)

        self.callActor.onCallEndTimer()
        
        self.sccpPhone.endCall.assert_called_once_with(7,34)
        

    def testAutoAnswer(self):
        self.callActor.setAutoAnswer(False)
        self.callActor.handleCall(1,34,SCCPCallState.SCCP_CHANNELSTATE_RINGING)
        self.sccpPhone.answerCall.assert_never_called()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()