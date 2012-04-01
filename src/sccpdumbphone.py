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


class SCCPDumbPhone():
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
    
    def createClient(self):
        log.info('creating sccp client factory')
        self.client = SCCPClientFactory(
                        self.on_sccp_connect_success,
                        self.on_sccp_connect_fail)

        self.client.handleUnknownMessage(self.onUnknownMessage)

        self.client.addHandler(SCCPMessageType.RegisterAckMessage,self.onRegisteredAck)

        self.client.addHandler(SCCPMessageType.CapabilitiesReqMessage,self.onCapabilitiesReq)
        self.client.addHandler(SCCPMessageType.OpenReceiveChannel, self.onOpenReceiveChannel)

        return self.client

    def onUnknownMessage(self,message):
        log.info('receive unkown message ' + message.toStr())

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
        
    def onRegisteredAck(self,registerAck):
        log.info("sccp phone registered")
        log.info("--          keepAliveInterval : " + `registerAck.keepAliveInterval`)
        log.info("--               dateTemplate : " + `registerAck.dateTemplate`)
        log.info("-- secondaryKeepAliveInterval : " + `registerAck.secondaryKeepAliveInterval`)
        self.createTimer(registerAck.keepAliveInterval,self.onKeepAliveTimer)
        self.onRegistered()

    def onOpenReceiveChannel(self,message):
        self.client.sendSccpMessage(SCCPOpenReceiveChannelAck(0, self.host, 40000, message.conferenceId))


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

