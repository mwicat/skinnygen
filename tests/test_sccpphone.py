'''
Created on Jun 20, 2011

@author: lebleu1
'''
from sccp.sccpbuttontemplatereq import SCCPButtonTemplateReq
from sccp.sccpcapabilities import SCCPCapabilitiesRes
from sccp.sccpcapabilitiesreq import SCCPCapabilitiesReq
from sccp.sccpregister import SCCPRegister
from sccp.sccpregisterack import SCCPRegisterAck
from sccp.sccpregisteravailablelines import SCCPRegisterAvailableLines
from sccp.sccptimedatereq import SCCPTimeDateReq
from sccpphone import SCCPPhone
from tests.mock import Mock
import unittest
from sccp.sccpdefinetimedate import SCCPDefineTimeDate
from sccp.sccpsetspeakermode import SCCPSetSpeakerMode
from sccp.sccpcallstate import SCCPCallState
from sccp.sccpkeypadbutton import SCCPKeyPadButton
from gui.softkeys import SKINNY_LBL_NEWCALL, SKINNY_LBL_ANSWER,\
    SKINNY_LBL_ENDCALL
from sccp.sccpsoftkeyevent import SCCPSoftKeyEvent
from sccp.sccpmessagetype import SCCPMessageType
from sccp.sccpmessage import SCCPMessage
from sccp.sccplinestat import SCCPLineStat
from sccp.sccplinestatreq import SCCPLineStatReq


        

class AnyInstanceOf(object):
    
    def __init__(self, clazz):
        self.clazz = clazz

    def __eq__(self,other):
        return self.clazz.__name__ == other.__class__.__name__
  
class TestSCCPPhone(unittest.TestCase):
    
    def log(self,msg):
        print(msg)

    def setUp(self):
        self.sccpPhone = SCCPPhone('1.1.1.1','SEP001166554433')
        self.sccpPhone.setLogger(self.log)


    def testOnConnectSuccess(self):

        networkClient = Mock()
        self.sccpPhone.client = networkClient
        self.sccpPhone.on_sccp_connect_success()
        registerMessage = SCCPRegister('SEP001166554433', "1.1.1.1")
        
        networkClient.sendSccpMessage.assert_called_with(registerMessage)


    def testOnRegisteredAck(self):
        registeredHandler = Mock()
        timerProvider = Mock()
        registerAck = SCCPRegisterAck()
        registerAck.keepAliveInterval=25
        
        self.sccpPhone.setTimerProvider(timerProvider)
        self.sccpPhone.setRegisteredHandler(registeredHandler)
        self.sccpPhone.onRegisteredAck(registerAck)
        timerProvider.createTimer.assert_called_with(25,self.sccpPhone.onKeepAliveTimer)
        registeredHandler.onRegistered.assert_called_with()
        
    def testOnKeepAliveTimer(self):
        networkClient = Mock()
        self.sccpPhone.client = networkClient
        keepaliveMessage = SCCPMessage(SCCPMessageType.KeepAliveMessage)
        
        self.sccpPhone.onKeepAliveTimer()
        networkClient.sendSccpMessage.assert_called_with(keepaliveMessage)
        
    def testOnCapabilitesReq(self):
        networkClient = Mock()
        self.sccpPhone.client = networkClient

        self.sccpPhone.onCapabilitiesReq(SCCPCapabilitiesReq())
       
        networkClient.sendSccpMessage.assert_was_called_with(AnyInstanceOf(SCCPCapabilitiesRes))
        networkClient.sendSccpMessage.assert_was_called_with(AnyInstanceOf(SCCPButtonTemplateReq))
        networkClient.sendSccpMessage.assert_was_called_with(AnyInstanceOf(SCCPLineStatReq))
        networkClient.sendSccpMessage.assert_was_called_with(AnyInstanceOf(SCCPRegisterAvailableLines))
        networkClient.sendSccpMessage.assert_was_called_with(AnyInstanceOf(SCCPTimeDateReq))
    
    def testOnDefineTimeDate(self):
        defineDateTime = SCCPDefineTimeDate()
        defineDateTime.day=21
        defineDateTime.month=6
        defineDateTime.year=2011
        defineDateTime.hour=11
        defineDateTime.minute=40
        defineDateTime.seconds=36
        
        dateTimePicker = Mock()

        self.sccpPhone.setDateTimePicker(dateTimePicker)
        self.sccpPhone.onDefineTimeDate(defineDateTime)
        dateTimePicker.setDateTime.assert_called_with(21,6,2011,11,40,36)
        
    def testOnSetSpeakerMode(self):
        self.sccpPhone.onSetSpeakerMode(SCCPSetSpeakerMode())
        
    def testOnCallState(self):
        callHandler1 = Mock()
        self.sccpPhone.addCallHandler(callHandler1)
        
        callHandler2 = Mock()
        self.sccpPhone.addCallHandler(callHandler2)

        callState = SCCPCallState()
        callState.callId=43
        callState.line=2
        callState.callState=SCCPCallState.SCCP_CHANNELSTATE_RINGING
        
        self.sccpPhone.onCallState(callState)
        
        callHandler1.handleCall.assert_called_with(2,43,SCCPCallState.SCCP_CHANNELSTATE_RINGING)
        callHandler2.handleCall.assert_called_with(2,43,SCCPCallState.SCCP_CHANNELSTATE_RINGING)
    
    def testOnDialPadNumericButtonPushed(self):
        networkClient = Mock()
        self.sccpPhone.client = networkClient
        dialPadMessage = SCCPKeyPadButton(int('1'))
        self.sccpPhone.onDialPadButtonPushed('1')
    
        networkClient.sendSccpMessage.assert_called_with(dialPadMessage)
         
    def testOnDialPadHashButtonPushed(self):
        networkClient = Mock()
        self.sccpPhone.client = networkClient
        dialPadMessage = SCCPKeyPadButton(15)
        self.sccpPhone.onDialPadButtonPushed('#')
    
        networkClient.sendSccpMessage.assert_called_with(dialPadMessage)

    def testOnDialPadStarButtonPushed(self):
        networkClient = Mock()
        self.sccpPhone.client = networkClient
        dialPadMessage = SCCPKeyPadButton(14)
        self.sccpPhone.onDialPadButtonPushed('*')
    
        networkClient.sendSccpMessage.assert_called_with(dialPadMessage)
        
        
    def testDial(self):
        networkClient = Mock()
        self.sccpPhone.client = networkClient
        
        newCallMessage = SCCPSoftKeyEvent(SKINNY_LBL_NEWCALL)

        self.sccpPhone.dial('12')
        
        networkClient.sendSccpMessage.assert_was_called_with(newCallMessage)
        networkClient.sendSccpMessage.assert_was_called_with(SCCPKeyPadButton(1))
        networkClient.sendSccpMessage.assert_was_called_with(SCCPKeyPadButton(2))
        
        
    def testOnSoftKeyNewCall(self):
        networkClient = Mock()
        self.sccpPhone.client = networkClient
        newCallMessage = SCCPSoftKeyEvent(SKINNY_LBL_NEWCALL)
        
        self.sccpPhone.onSoftKey(SKINNY_LBL_NEWCALL)

        networkClient.sendSccpMessage.assert_was_called_with(newCallMessage)

    def testOnSoftKeyAnswerCall(self):
        networkClient = Mock()
        self.sccpPhone.client = networkClient
        
        callState = SCCPCallState()
        callState.callId=43
        callState.line=2
        callState.callState=SCCPCallState.SCCP_CHANNELSTATE_RINGING
        
        self.sccpPhone.onCallState(callState)

        answerCallMessage = SCCPSoftKeyEvent(SKINNY_LBL_ANSWER,2,43)
        
        self.sccpPhone.onSoftKey(SKINNY_LBL_ANSWER)

        networkClient.sendSccpMessage.assert_was_called_with(answerCallMessage)
        
    def testOnLineStat(self):
        lineStatMessage = SCCPLineStat()
        lineStatMessage.line = 1
        lineStatMessage.dirNumber = '2034'
        displayHandler = Mock()
        self.sccpPhone.setDisplayHandler(displayHandler)
        
        self.sccpPhone.onLineStat(lineStatMessage)

        displayHandler.displayLineInfo.assert_called_with(1,'2034')
        
    
    def testAnswerCall(self):
        networkClient = Mock()
        self.sccpPhone.client = networkClient

        callState = SCCPCallState()
        callState.callId=43
        callState.line=2
        callState.callState=SCCPCallState.SCCP_CHANNELSTATE_RINGING
        
        self.sccpPhone.onCallState(callState)

        answerCallMessage = SCCPSoftKeyEvent(SKINNY_LBL_ANSWER,2,43)

        
        self.sccpPhone.answerCall()

        networkClient.sendSccpMessage.assert_was_called_with(answerCallMessage)
        
        
    def testHangupCall(self):
        networkClient = Mock()
        self.sccpPhone.client = networkClient


        endCallMessage = SCCPSoftKeyEvent(SKINNY_LBL_ENDCALL,3,54)

        
        self.sccpPhone.endCall(3,54)

        networkClient.sendSccpMessage.assert_was_called_with(endCallMessage)
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()