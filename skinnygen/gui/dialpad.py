'''
Created on Jun 16, 2011

@author: lebleu1
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class DialPad(QVBoxLayout):
    '''
    classdocs
    '''

    def __init__(self, showDialPad=True):
        QVBoxLayout.__init__(self)
        self.createDialEditBox()
        self.dialPadBox = QVBoxLayout()
        if (showDialPad):
            self.addLayout(self.dialPadBox)
        self.createButtonRange(1)
        self.createButtonRange(4)
        self.createButtonRange(7)
        self.createLastRange()

    def connectPad(self,padHandler):
        self.padHandler = padHandler
   
    def createDialEditBox(self):
        editBox = QHBoxLayout()
        self.numberEdit = QComboBox()
        self.numberEdit.acceptDrops()
        self.numberEdit.setEditable(True)
        editBox.addWidget(self.numberEdit)
        dialButton = QPushButton('Dial');
        dialButton.clicked.connect(self.onDialButton)
        dialButton.setMaximumWidth(50)
        editBox.addWidget(dialButton)
        self.addLayout(editBox)
 
    def createButtonRange(self,start):
        buttonBox = QHBoxLayout()
        for i in range(3):
            self.createButton(buttonBox,str(i+start))
        self.dialPadBox.addLayout(buttonBox)
        
    def createLastRange(self):
        buttonBox = QHBoxLayout()
        self.createButton(buttonBox, '*')
        self.createButton(buttonBox, '0')
        self.createButton(buttonBox, '#')
        self.dialPadBox.addLayout(buttonBox)

        
    def createButton(self,layout,label):
        button = QPushButton(label);
        layout.addWidget(button)
        button.clicked.connect(self.onDialPadButton)

    def onDialPadButton(self):
        self.numberEdit.setEditText(str(self.numberEdit.currentText())+str(self.sender().text()))
        self.padHandler.onDialPadButtonPushed(str(self.sender().text()))
        
    def onDialButton(self):
        numberToDial = str(self.numberEdit.currentText())
        self.padHandler.dial(numberToDial)
        self.numberEdit.addItem(numberToDial)
    
        
        
    
