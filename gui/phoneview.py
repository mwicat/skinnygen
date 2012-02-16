'''
Created on Jun 21, 2011

@author: lebleu1
'''
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from gui.connectindicator import ConnectIndicator
from gui.calldisplay import CallDisplay
from gui.softkeys import SoftKeys
from gui.dialpad import DialPad

class PhoneView(QVBoxLayout):
    '''
    classdocs
    '''


    def __init__(self,serverHost,deviceName,connectHandler):
        QVBoxLayout.__init__(self)
        self.serverHost = serverHost
        self.deviceName = deviceName
        self.connectHandler=connectHandler
        self.createView()
 
 
    def createView(self):
        self.create_time_box()
        
        self.callDisplay = CallDisplay()
        self.addLayout(self.callDisplay)

        self.softKeys = SoftKeys()
        self.addLayout(self.softKeys)

        self.dialPad = DialPad(False)
        self.addLayout(self.dialPad)

        self.createDeviceParameters()
        
        self.connectButton = QPushButton('Connect !')
        self.connectButton.clicked.connect(self.onConnect)
        self.addWidget(self.connectButton)
 
        
        
    def create_time_box(self):
        timeBox = QHBoxLayout()
        self.timeDateLabel = QLabel('..................')
        timeBox.addWidget(self.timeDateLabel)
        self.lineLabel = QLabel('---------------')
        timeBox.addWidget(self.lineLabel)
        self.connectIndicator = ConnectIndicator()
        timeBox.addWidget(self.connectIndicator)

        self.addLayout(timeBox)        
        
        
    def createDeviceParameters(self):
        hostBox = QHBoxLayout()
        deviceNameLabel = QLabel("Phone Set : ")
        self.deviceNameEdit = QLineEdit()
        self.deviceNameEdit.setText(self.deviceName)
        hostBox.addWidget(deviceNameLabel)
        hostBox.addWidget(self.deviceNameEdit)
        self.addLayout(hostBox)
        
    def onConnect(self):
        self.sccpPhone.host=self.serverHost
        self.sccpPhone.deviceName=str(self.deviceNameEdit.text())        
        self.connectHandler(self.sccpPhone.host,self.sccpPhone.deviceName,self.sccpPhone.client)
        
    def setDateTime(self,day,month,year,hour,minute,seconds):
        self.timeDateLabel.setText(`day` + '-'+`month` + '-' + `year` 
                                   + ' ' +`hour`+':'+`minute`+':'+`seconds`)
        
    def displayLineInfo(self,line,dirNumber):
        self.lineLabel.setText(`line`+' : ' +`dirNumber`)
        
    def handleCall(self,line,callId,callState):
        self.callDisplay.displayCall(line, callId, callState)
        
    def useSccpPhone(self,sccpPhone):
        self.sccpPhone = sccpPhone
        self.sccpPhone.setDateTimePicker(self)
        self.sccpPhone.setDisplayHandler(self)
        self.sccpPhone.addCallHandler(self)
        self.sccpPhone.setRegisteredHandler(self)
        self.dialPad.connectPad(self.sccpPhone)
        self.softKeys.connectSoftKeys(self.sccpPhone.onSoftKey)
        self.sccpPhone.createClient()
        


    def onRegistered(self):
        self.connectIndicator.connected = True
         
        