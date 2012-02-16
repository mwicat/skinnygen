'''
Created on Jun 17, 2011

@author: lebleu1
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *

SKINNY_LBL_EMPTY = 0
SKINNY_LBL_REDIAL = 1
SKINNY_LBL_NEWCALL = 2
SKINNY_LBL_HOLD = 3
SKINNY_LBL_TRANSFER = 4
SKINNY_LBL_CFWDALL = 5
SKINNY_LBL_CFWDBUSY = 6
SKINNY_LBL_CFWDNOANSWER = 7
SKINNY_LBL_BACKSPACE = 8
SKINNY_LBL_ENDCALL = 9
SKINNY_LBL_RESUME = 10
SKINNY_LBL_ANSWER = 11

SKINNY_LBL_RINGOUT = 34
SKINNY_LBL_DIAL = 101


SOFT_KEYS_LABELS_TO_EVENT={
                           'Redial' : SKINNY_LBL_REDIAL,
                           'NewCall' : SKINNY_LBL_NEWCALL,
                           'Hold' : SKINNY_LBL_HOLD,
                           'Transfer' :SKINNY_LBL_TRANSFER,
                           'EndCall' : SKINNY_LBL_ENDCALL,
                           'Answer' : SKINNY_LBL_ANSWER 
                           }


class SoftKeys(QVBoxLayout):

    def __init__(self, *args, **kwargs):
        QVBoxLayout.__init__(self, *args, **kwargs)
        self.createSoftKeyButtons()
 
    def connectSoftKeys(self,softKeyHandler):
        self.softKeyHandler = softKeyHandler
       
        
    def createSoftKeyButtons(self):
        mainBox=QVBoxLayout()
        buttonBox =QHBoxLayout()
        mainBox.addLayout(buttonBox)
        buttonBox.setAlignment(Qt.AlignCenter)
        self.createSoftKey(buttonBox,'NewCall')
        self.createSoftKey(buttonBox,'EndCall')
        self.createSoftKey(buttonBox,'Answer')
        buttonBox =QHBoxLayout()
        mainBox.addLayout(buttonBox)
        buttonBox.setAlignment(Qt.AlignCenter)        
        self.createSoftKey(buttonBox,'Redial')
        self.createSoftKey(buttonBox,'Hold')
        self.createSoftKey(buttonBox,'Transfer')
        self.addLayout(mainBox)
                
    def createSoftKey(self,layout,content):
        key = QPushButton(str(content))
        key.setStyleSheet("background-color: #0099FF")
        key.clicked.connect(self.onSoftKey)
        layout.addWidget(key)
        
    def onSoftKey(self):
        event = SOFT_KEYS_LABELS_TO_EVENT[str(self.sender().text())]
        self.softKeyHandler(event)
          


