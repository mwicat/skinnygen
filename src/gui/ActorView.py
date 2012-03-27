'''
Created on Jun 29, 2011

@author: lebleu1
'''

from PyQt4.QtGui import *

class ActorView(QVBoxLayout):


    def __init__(self,callActor):
        QVBoxLayout.__init__(self)
        self.callActor = callActor 
        box = QGroupBox('Actor')
        layout = QVBoxLayout()
        box.setLayout(layout)
        self.addWidget(box)
        self.autoAnswer = QCheckBox('Auto Answer')
        self.autoAnswer.clicked.connect(self.changeAutoAnswer)
        self.autoAnswer.setCheckState(self.callActor.getAutoAnswer())
        layout.addWidget(self.autoAnswer)
        
        
    def changeAutoAnswer(self):
        self.callActor.setAutoAnswer(self.autoAnswer.checkState())