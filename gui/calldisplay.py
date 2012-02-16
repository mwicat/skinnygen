'''
Created on Jun 20, 2011

@author: lebleu1
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from sccp.sccpcallstate import SCCPCallState


class CallDisplay(QHBoxLayout):

    def __init__(self, *args, **kwargs):
        QHBoxLayout.__init__(self, *args, **kwargs)
        self.line = QLabel('Line :')
        self.addWidget(self.line)
        self.callId = QLabel('CallId :')
        self.addWidget(self.callId)
        self.callState = QLabel('State :')
        self.addWidget(self.callState)



    def displayCall(self,line,callId,callState):
        self.line.setText('Line : ' + str(line))
        self.callId.setText('CallId :' + str(callId))
        self.callState.setText(SCCPCallState.sccp_channelstates[callState])