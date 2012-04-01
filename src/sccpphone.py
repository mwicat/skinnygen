'''
Created on Jun 20, 2011

@author: lebleu1
'''
from network.sccpclientfactory import SCCPClientFactory
from sccp.sccpmessagetype import SCCPMessageType
from sccp.sccpregister import SCCPRegister
from sccp.sccpcapabilities import SCCPCapabilitiesRes
from sccp.sccpbuttontemplatereq import SCCPButtonTemplateReq
from sccp.sccpregisteravailablelines import SCCPRegisterAvailableLines
from sccp.sccptimedatereq import SCCPTimeDateReq
from sccp.sccpcallstate import SCCPCallState
from sccp.sccpkeypadbutton import SCCPKeyPadButton
from sccp.sccpsoftkeyevent import SCCPSoftKeyEvent
from sccp.sccpopenreceivechannelack import SCCPOpenReceiveChannelAck
from gui.softkeys import SKINNY_LBL_NEWCALL, SKINNY_LBL_ANSWER,\
    SKINNY_LBL_ENDCALL
from sccp.sccpmessage import SCCPMessage
from sccp.sccplinestatreq import SCCPLineStatReq

import logging
log = logging.getLogger(__name__)


class SCCPPhone():
    '''
    Main sccp phone class
    '''


    def __init__(self,host,deviceName):
        self.host = host
        self.deviceName = deviceName
        self.callHandlers = set()
        self.toneHandler = None
        self.softKeysHandler = None
        
    def setLogger(self,logger):
        self.log = logger
    
    def setTimerProvider(self,timerProvider):
        self.timerProvider = timerProvider

    
    def setRegisteredHandler(self,registeredHandler):
        self.registeredHandler = registeredHandler

    def setToneHandler(self,toneHandler):
        self.toneHandler = toneHandler
        
    def setDateTimePicker(self,dateTimePicker):
        self.dateTimePicker = dateTimePicker

    def setDisplayHandler(self,displayHandler):
        self.displayHandler = displayHandler

    def setSoftKeysHandler(self,softKeysHandler):
        self.softKeysHandler = softKeysHandler

    def setDisplayPromptStatusHandler(self,displayPromptStatusHandler):
        self.displayPromptStatusHandler = displayPromptStatusHandler

    def setSetRingerHandler(self,setRingerHandler):
        self.setRingerHandler = setRingerHandler
        
    def addCallHandler(self,callHandler):
        log.info(self.deviceName + ' adding call handler')
        self.callHandlers.add(callHandler)
        
    def createClient(self):
        log.info('creating sccp client factory')
        self.client = SCCPClientFactory(
                        self.on_sccp_connect_success,
                        self.on_sccp_connect_fail)

        self.client.handleUnknownMessage(self.onUnknownMessage)

        self.client.addHandler(SCCPMessageType.RegisterAckMessage,self.onRegisteredAck)
        self.client.addHandler(SCCPMessageType.KeepAliveAckMessage,self.onKeepAliveAck)

        self.client.addHandler(SCCPMessageType.CapabilitiesReqMessage,self.onCapabilitiesReq)
        self.client.addHandler(SCCPMessageType.OpenReceiveChannel, self.onOpenReceiveChannel)

        self.client.addHandler(SCCPMessageType.DefineTimeDate,self.onDefineTimeDate)
        self.client.addHandler(SCCPMessageType.SetSpeakerModeMessage,self.onSetSpeakerMode)
        self.client.addHandler(SCCPMessageType.CallStateMessage,self.onCallState)
        self.client.addHandler(SCCPMessageType.ActivateCallPlaneMessage,self.onActivateCallPlane)
        self.client.addHandler(SCCPMessageType.StartToneMessage,self.onStartTone)
        self.client.addHandler(SCCPMessageType.LineStatMessage,self.onLineStat)
        self.client.addHandler(SCCPMessageType.SetRingerMessage, self.onSetRinger)
        self.client.addHandler(SCCPMessageType.DisplayPromptStatusMessage, self.onDisplayPromptStatus)
        self.client.addHandler(SCCPMessageType.SelectSoftKeysMessage, self.onSelectSoftKeys)

        return self.client

    def on_sccp_connect_success(self):
        log.info('Connected to server. Sending register with phone set : ' + self.deviceName)
        registerMessage = SCCPRegister(self.deviceName, self.host)
        self.client.sendSccpMessage(registerMessage)
        
    def on_sccp_connect_fail(self, reason):
        # reason is a twisted.python.failure.Failure  object
        log.info('Connection failed: %s' % reason.getErrorMessage())
        
    def onKeepAliveTimer(self):
        log.info('on keep alive')
        message = SCCPMessage(SCCPMessageType.KeepAliveMessage)
        self.client.sendSccpMessage(message)
        
    def onUnknownMessage(self,message):
        log.info('receive unkown message ' + message.toStr())

    def onRegisteredAck(self,registerAck):
        log.info("sccp phone registered")
        log.info("--          keepAliveInterval : " + `registerAck.keepAliveInterval`)
        log.info("--               dateTemplate : " + `registerAck.dateTemplate`)
        log.info("-- secondaryKeepAliveInterval : " + `registerAck.secondaryKeepAliveInterval`)
        self.timerProvider.createTimer(registerAck.keepAliveInterval,self.onKeepAliveTimer)
        self.registeredHandler.onRegistered()

        
    def onKeepAliveAck(self,message):
        log.info("Keepalive ack")
    
    def onCapabilitiesReq(self,message):
        log.info("sending capabilities response")
        self.client.sendSccpMessage(SCCPCapabilitiesRes())
        log.info("sending button template request message")
        self.client.sendSccpMessage(SCCPButtonTemplateReq())
        log.info("sending line status request message")
        self.client.sendSccpMessage(SCCPLineStatReq(1))
        log.info("sending register available lines")
        self.client.sendSccpMessage(SCCPRegisterAvailableLines())
        log.info("sending time date request message")
        self.client.sendSccpMessage(SCCPTimeDateReq())

        
    def onDefineTimeDate(self,message):
        log.info('define time and date')
        self.dateTimePicker.setDateTime(message.day,message.month,message.year,message.hour,message.minute,message.seconds)
    
    def onSetSpeakerMode(self,message):
        log.info('set speaker mode '+`message.mode`)

    def onCallState(self,message):
        log.info('call state line : ' + `message.line` + ' for callId '+ `message.callId` + ' is ' + SCCPCallState.sccp_channelstates[message.callState])
        self.currentLine = message.line
        self.currentCallId=message.callId
        self.callState=message.callState
        
        for callHandler in self.callHandlers:
            callHandler.handleCall(message.line,message.callId,message.callState)
        
    def onLineStat(self,message):
        log.info('line stat ' + `message.line` + ' : ' + `message.dirNumber`)
        self.displayHandler.displayLineInfo(message.line,message.dirNumber)

    def onSetRinger(self,message):
        self.setRingerHandler.onSetRinger(message.ringType, message.ringMode, message.line, message.callId)

    def onDisplayPromptStatus(self,message):
        self.displayPromptStatusHandler.onDisplayPromptStatus(message.displayMessage, message.line, message.callId)

    def onStartTone(self,message):
        log.info('start tone : '+`message.tone` + ' timeout ' + `message.toneTimeout` + ' line ' + `message.line` + ' for callId '+ `message.callId`)
        if self.toneHandler is not None:
            self.toneHandler.handleTone(message.line,message.callId,message.tone)

    def onSelectSoftKeys(self,message):
        if self.softKeysHandler is not None:
            self.softKeysHandler.handleSoftKeys(message.line,message.callId,message.softKeySet, message.softKeyMap)

    def onOpenReceiveChannel(self,message):
        self.client.sendSccpMessage(SCCPOpenReceiveChannelAck(0, self.host, 40000, message.conferenceId))

    def onActivateCallPlane(self,message):
        log.info('Activate call plane on line '+`message.line`)
        
    def onDialPadButtonPushed(self,car):
        log.info("dialed : " + car)
        if (car == '#'):
            event = 15
        elif (car == '*'):
            event = 14
        else:
            event = int(car)
        message = SCCPKeyPadButton(event)
        self.client.sendSccpMessage(message)
        
    def dial(self,numberToDial):
        log.info('dialing : '+numberToDial)
        self.client.sendSccpMessage(SCCPSoftKeyEvent(SKINNY_LBL_NEWCALL))
        for digit in numberToDial:
            self.onDialPadButtonPushed(digit)
            
    def onSoftKey(self,event):
        log.info('on soft key '+`event`)
        if (event != SKINNY_LBL_NEWCALL):
            message = SCCPSoftKeyEvent(event,self.currentLine,self.currentCallId)
        else:
            message = SCCPSoftKeyEvent(event)
        self.client.sendSccpMessage(message)
        
    def answerCall(self):
        self.onSoftKey(SKINNY_LBL_ANSWER)
        
    def endCall(self,line,callId):
        message = SCCPSoftKeyEvent(SKINNY_LBL_ENDCALL,line,callId)
        self.client.sendSccpMessage(message)
