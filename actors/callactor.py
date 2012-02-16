'''
Created on Jun 28, 2011

@author: lebleu1
'''
from sccp.sccpcallstate import SCCPCallState
import random


class CallActor():
    
    callDurationMin = 2
    callDurationMax = 10
    autoAnswer = False
    currentCallState = SCCPCallState.SCCP_CHANNELSTATE_ONHOOK
    currentCallId = 0
    currentLine= 0
    
    def setPhone(self,phone):
        self.phone = phone
        
    def setTimerProvider(self,timerProvider):
        self.timerProvider = timerProvider
        
    def getAutoAnswer(self):
        return self.autoAnswer
    
    def setAutoAnswer(self,autoAnswer):
        self.autoAnswer = autoAnswer
        
                
    def handleCall(self,line,callid,callState):
        if not self.autoAnswer:
            return
        if callState == SCCPCallState.SCCP_CHANNELSTATE_RINGING:
                if self.currentCallId == 0:
                    self.phone.answerCall()
                    self.currentCallId = callid
                    self.currentLine = line
        if callState == SCCPCallState.SCCP_CHANNELSTATE_CONNECTED:
            timerInSec = random.randrange(self.callDurationMin,self.callDurationMax)
            self.timerProvider.createOneShotTimer(timerInSec,self.onCallEndTimer)
            
        if callState == SCCPCallState.SCCP_CHANNELSTATE_ONHOOK and self.currentCallId == callid:
            self.currentCallId = 0

        self.currentCallState = callState
            
            
            
    def onCallEndTimer(self):
        self.phone.endCall(self.currentLine,self.currentCallId)
