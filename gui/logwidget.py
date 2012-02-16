from PyQt4.QtCore import *
from PyQt4.QtGui import *



class LogWidget(QTextBrowser):
    def __init__(self, parent=None):
        super(LogWidget, self).__init__(parent)
        palette = QPalette()
        palette.setColor(QPalette.Base, QColor("#ddddfd"))
        self.setPalette(palette)
    def minimumSizeHint(self, *args, **kwargs):
        return QSize(200,300)
