'''
Created on Jun 10, 2011

@author: lebleu1
'''
import struct

MESSAGES_NAMES = dict([
  (0x0000, "KeepAliveMessage"),
  (0x0001, "RegisterMessage"),
  (0x0002, "IpPortMessage"),
  (0x0003, "KeypadButtonMessage"),
  (0x0004, "EnblocCallMessage"),
  (0x0005, "StimulusMessage"),
  (0x0006, "OffHookMessage"),
  (0x0007, "OnHookMessage"),
  (0x0008, "HookFlashMessage"),
  (0x0009, "ForwardStatReqMessage"),
  (0x000A, "SpeedDialStatReqMessage"),
  (0x000B, "LineStatReqMessage"),
  (0x000C, "ConfigStatReqMessage"),
  (0x000D, "TimeDateReqMessage"),
  (0x000E, "ButtonTemplateReqMessage"),
  (0x000F, "VersionReqMessage"),
  (0x0010, "CapabilitiesResMessage"),
  (0x0011, "MediaPortListMessage"),
  (0x0012, "ServerReqMessage"),
  (0x0020, "AlarmMessage"),
  (0x0021, "MulticastMediaReceptionAck"),
  (0x0022, "OpenReceiveChannelAck"),
  (0x0023, "ConnectionStatisticsRes"),
  (0x0024, "OffHookWithCgpnMessage"),
  (0x0025, "SoftKeySetReqMessage"),
  (0x0026, "SoftKeyEventMessage"),
  (0x0027, "UnregisterMessage"),
  (0x0028, "SoftKeyTemplateReqMessage"),
  (0x0029, "RegisterTokenReq"),
  (0x002A, "MediaTransmissionFailure"),
  (0x002B, "HeadsetStatusMessage"),
  (0x002C, "MediaResourceNotification"),
  (0x002D, "RegisterAvailableLinesMessage"),
  (0x002E, "DeviceToUserDataMessage"),
  (0x002F, "DeviceToUserDataResponseMessage"),
  (0x0030, "UpdateCapabilitiesMessage"),
  (0x0031, "OpenMultiMediaReceiveChannelAckMessage"),
  (0x0032, "ClearConferenceMessage"),
  (0x0033, "ServiceURLStatReqMessage"),
  (0x0034, "FeatureStatReqMessage"),
  (0x0035, "CreateConferenceResMessage"),
  (0x0036, "DeleteConferenceResMessage"),
  (0x0037, "ModifyConferenceResMessage"),
  (0x0038, "AddParticipantResMessage"),
  (0x0039, "AuditConferenceResMessage"),
  (0x0040, "AuditParticipantResMessage"),
  (0x0041, "DeviceToUserDataVersion1Message"),
  (0x0042, "DeviceToUserDataResponseVersion1Message"),

  (0x0081, "RegisterAckMessage"),
  (0x0082, "StartToneMessage"),
  (0x0083, "StopToneMessage"),
  (0x0085, "SetRingerMessage"),
  (0x0086, "SetLampMessage"),
  (0x0087, "SetHkFDetectMessage"),
  (0x0088, "SetSpeakerModeMessage"),
  (0x0089, "SetMicroModeMessage"),
  (0x008A, "StartMediaTransmission"),
  (0x008B, "StopMediaTransmission"),
  (0x008C, "StartMediaReception"),
  (0x008D, "StopMediaReception"),
  (0x008F, "CallInfoMessage"),
  (0x0090, "ForwardStatMessage"),
  (0x0091, "SpeedDialStatMessage"),
  (0x0092, "LineStatMessage"),
  (0x0093, "ConfigStatMessage"),
  (0x0094, "DefineTimeDate"),
  (0x0095, "StartSessionTransmission"),
  (0x0096, "StopSessionTransmission"),
  (0x0097, "ButtonTemplateMessage"),
  (0x0098, "VersionMessage"),
  (0x0099, "DisplayTextMessage"),
  (0x009A, "ClearDisplay"),
  (0x009B, "CapabilitiesReqMessage"),
  (0x009C, "EnunciatorCommandMessage"),
  (0x009D, "RegisterRejectMessage"),
  (0x009E, "ServerResMessage"),
  (0x009F, "Reset"),
  (0x0100, "KeepAliveAckMessage"),
  (0x0101, "StartMulticastMediaReception"),
  (0x0102, "StartMulticastMediaTransmission"),
  (0x0103, "StopMulticastMediaReception"),
  (0x0104, "StopMulticastMediaTransmission"),
  (0x0105, "OpenReceiveChannel"),
  (0x0106, "CloseReceiveChannel"),
  (0x0107, "ConnectionStatisticsReq"),
  (0x0108, "SoftKeyTemplateResMessage"),
  (0x0109, "SoftKeySetResMessage"),
  (0x0110, "SelectSoftKeysMessage"),
  (0x0111, "CallStateMessage"),
  (0x0112, "DisplayPromptStatusMessage"),
  (0x0113, "ClearPromptStatusMessage"),
  (0x0114, "DisplayNotifyMessage"),
  (0x0115, "ClearNotifyMessage"),
  (0x0116, "ActivateCallPlaneMessage"),
  (0x0117, "DeactivateCallPlaneMessage"),
  (0x0118, "UnregisterAckMessage"),
  (0x0119, "BackSpaceReqMessage"),
  (0x011A, "RegisterTokenAck"),
  (0x011B, "RegisterTokenReject"),

  (0x011C, "StartMediaFailureDetection"),
  (0x011D, "DialedNumberMessage"),
  (0x011E, "UserToDeviceDataMessage"),
  (0x011F, "FeatureStatMessage"),
  (0x0120, "DisplayPriNotifyMessage"),
  (0x0121, "ClearPriNotifyMessage"),
  (0x0122, "StartAnnouncementMessage"),
  (0x0123, "StopAnnouncementMessage"),
  (0x0124, "AnnouncementFinishMessage"),
  (0x0127, "NotifyDtmfToneMessage"),
  (0x0128, "SendDtmfToneMessage"),
  (0x0129, "SubscribeDtmfPayloadReqMessage"),
  (0x012A, "SubscribeDtmfPayloadResMessage"),
  (0x012B, "SubscribeDtmfPayloadErrMessage"),
  (0x012C, "UnSubscribeDtmfPayloadReqMessage"),
  (0x012D, "UnSubscribeDtmfPayloadResMessage"),
  (0x012E, "UnSubscribeDtmfPayloadErrMessage"),
  (0x012F, "ServiceURLStatMessage"),
  (0x0130, "CallSelectStatMessage"),
  (0x0131, "OpenMultiMediaChannelMessage"),
  (0x0132, "StartMultiMediaTransmission"),
  (0x0133, "StopMultiMediaTransmission"),
  (0x0134, "MiscellaneousCommandMessage"),
  (0x0135, "FlowControlCommandMessage"),
  (0x0136, "CloseMultiMediaReceiveChannel"),
  (0x0137, "CreateConferenceReqMessage"),
  (0x0138, "DeleteConferenceReqMessage"),
  (0x0139, "ModifyConferenceReqMessage"),
  (0x013A, "AddParticipantReqMessage"),
  (0x013B, "DropParticipantReqMessage"),
  (0x013C, "AuditConferenceReqMessage"),
  (0x013D, "AuditParticipantReqMessage"),
  (0x013F, "UserToDeviceDataVersion1Message")
  ])


class SCCPMessage:
    '''
    Sccp message
    '''

    def __init__(self,sccpMessageType):
        self.sccpmessageType = sccpMessageType
        self.sccpmessageName = MESSAGES_NAMES.get(sccpMessageType)
        self.reserved=0x00
    
    def __eq__(self,other):
        if (self.__class__.__name__ != other.__class__.__name__):
            return False
        return self.sccpmessageType == other.sccpmessageType

    def pack(self):
        return struct.pack("II",self.reserved,self.sccpmessageType)
    
    def unPack(self,buffer):
        self.buffer = buffer
        
    def toStr(self):
        return "SCCPMessage : %s (%s)" % (self.sccpmessageName, hex(self.sccpmessageType))
