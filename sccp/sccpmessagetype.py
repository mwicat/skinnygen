'''
Created on Jun 10 2011

@author: lebleu1
'''

class SCCPMessageType:
    '''
    SCCP Message types
    '''

    KeepAliveMessage = 0x0000
    RegisterMessage = 0x0001
    IpPortMessage = 0x0002
    KeypadButtonMessage = 0x0003
    EnblocCallMessage = 0x0004
    StimulusMessage = 0x0005
    OffHookMessage = 0x0006
    OnHookMessage = 0x0007
    HookFlashMessage = 0x0008
    ForwardStatReqMessage = 0x0009
    SpeedDialStatReqMessage = 0x000A
    LineStatReqMessage = 0x000B
    ConfigStatReqMessage = 0x000C
    TimeDateReqMessage = 0x000D
    ButtonTemplateReqMessage = 0x000E
    VersionReqMessage = 0x000F
    CapabilitiesResMessage = 0x0010
    MediaPortListMessage = 0x0011
    ServerReqMessage = 0x0012
    AlarmMessage = 0x0020
    MulticastMediaReceptionAck = 0x0021
    OpenReceiveChannelAck = 0x0022
    ConnectionStatisticsRes = 0x0023
    OffHookWithCgpnMessage = 0x0024
    SoftKeySetReqMessage = 0x0025
    SoftKeyEventMessage = 0x0026
    UnregisterMessage = 0x0027
    SoftKeyTemplateReqMessage = 0x0028
    RegisterTokenReq = 0x0029
    HeadsetStatusMessage = 0x002B
    MediaResourceNotification = 0x002C
    RegisterAvailableLinesMessage = 0x002D
    DeviceToUserDataMessage = 0x002E
    DeviceToUserDataResponseMessage = 0x002F
    UpdateCapabilitiesMessage = 0x0030
    OpenMultiMediaReceiveChannelAckMessage = 0x0031
    ClearConferenceMessage = 0x0032
    ServiceURLStatReqMessage = 0x0033
    FeatureStatReqMessage = 0x0034
    CreateConferenceResMessage = 0x0035
    DeleteConferenceResMessage = 0x0036
    ModifyConferenceResMessage = 0x0037
    AddParticipantResMessage = 0x0038
    AuditConferenceResMessage = 0x0039
    AuditParticipantResMessage = 0x0040
    DeviceToUserDataVersion1Message = 0x0041
    DeviceToUserDataResponseVersion1Message = 0x0042

    # This are from protocol V 11 CCM7 
    DialedPhoneBookMessage = 0x0048
    AccessoryStatusMessage = 0x0049
    Unknown_0x004A_Message = 0x004A

    # Server -> Client */
    RegisterAckMessage = 0x0081
    StartToneMessage = 0x0082
    StopToneMessage = 0x0083
    # ??
    SetRingerMessage = 0x0085
    SetLampMessage = 0x0086
    SetHkFDetectMessage = 0x0087
    SetSpeakerModeMessage = 0x0088
    SetMicroModeMessage = 0x0089
    StartMediaTransmission = 0x008A
    StopMediaTransmission = 0x008B
    StartMediaReception = 0x008C
    StopMediaReception = 0x008D
    # ?
    CallInfoMessage = 0x008F

    ForwardStatMessage = 0x0090
    SpeedDialStatMessage = 0x0091
    LineStatMessage = 0x0092
    ConfigStatMessage = 0x0093
    DefineTimeDate = 0x0094
    StartSessionTransmission = 0x0095
    StopSessionTransmission = 0x0096
    ButtonTemplateMessage = 0x0097
    ButtonTemplateMessageSingle = 0x0097
    VersionMessage = 0x0098
    DisplayTextMessage = 0x0099
    ClearDisplay = 0x009A
    CapabilitiesReqMessage = 0x009B
    EnunciatorCommandMessage = 0x009C
    RegisterRejectMessage = 0x009D
    ServerResMessage = 0x009E
    Reset = 0x009F

    KeepAliveAckMessage = 0x0100
    StartMulticastMediaReception = 0x0101
    StartMulticastMediaTransmission = 0x0102
    StopMulticastMediaReception = 0x0103
    StopMulticastMediaTransmission = 0x0104
    OpenReceiveChannel = 0x0105
    CloseReceiveChannel = 0x0106
    ConnectionStatisticsReq = 0x0107
    SoftKeyTemplateResMessage = 0x0108
    SoftKeySetResMessage = 0x0109

    SelectSoftKeysMessage = 0x0110
    CallStateMessage = 0x0111
    DisplayPromptStatusMessage = 0x0112
    ClearPromptStatusMessage = 0x0113
    DisplayNotifyMessage = 0x0114
    ClearNotifyMessage = 0x0115
    ActivateCallPlaneMessage = 0x0116
    DeactivateCallPlaneMessage = 0x0117
    UnregisterAckMessage = 0x0118
    BackSpaceReqMessage = 0x0119
    RegisterTokenAck = 0x011A
    RegisterTokenReject = 0x011B
    StartMediaFailureDetection = 0x011C
    DialedNumberMessage = 0x011D
    UserToDeviceDataMessage = 0x011E
    FeatureStatMessage = 0x011F
    DisplayPriNotifyMessage = 0x0120
    ClearPriNotifyMessage = 0x0121
    StartAnnouncementMessage = 0x0122
    StopAnnouncementMessage = 0x0123
    AnnouncementFinishMessage = 0x0124
    NotifyDtmfToneMessage = 0x0127
    SendDtmfToneMessage = 0x0128
    SubscribeDtmfPayloadReqMessage = 0x0129
    SubscribeDtmfPayloadResMessage = 0x012A
    SubscribeDtmfPayloadErrMessage = 0x012B
    UnSubscribeDtmfPayloadReqMessage = 0x012C
    UnSubscribeDtmfPayloadResMessage = 0x012D
    UnSubscribeDtmfPayloadErrMessage = 0x012E
    ServiceURLStatMessage = 0x012F
    CallSelectStatMessage = 0x0130
    OpenMultiMediaChannelMessage = 0x0131
    StartMultiMediaTransmission = 0x0132
    StopMultiMediaTransmission = 0x0133
    MiscellaneousCommandMessage = 0x0134
    FlowControlCommandMessage = 0x0135
    CloseMultiMediaReceiveChannel = 0x0136
    CreateConferenceReqMessage = 0x0137
    DeleteConferenceReqMessage = 0x0138
    ModifyConferenceReqMessage = 0x0139
    AddParticipantReqMessage = 0x013A
    DropParticipantReqMessage = 0x013B
    AuditConferenceReqMessage = 0x013C
    AuditParticipantReqMessage = 0x013D
    UserToDeviceDataVersion1Message = 0x013F

    # sent by us */
    Unknown_0x0141_Message = 0x0141
    Unknown_0x0143_Message = 0x0143
    Unknown_0x0144_Message = 0x0144
    DisplayDynamicPromptStatusMessage = 0x0145
    FeatureStatAdvancedMessage = 0x0146
    LineStatDynamicMessage = 0x0147
    ServiceURLStatDynamicMessage = 0x0148
    SpeedDialStatDynamicMessage = 0x0149
    CallInfoDynamicMessage = 0x014A

    # received from phone */
    DialedPhoneBookAckMessage = 0x0152
    Unknown_0x0153_Message = 0x0153
    StartMediaTransmissionAck = 0x0154
    ExtensionDeviceCaps = 0x0159
    XMLAlarmMessage = 0x015A