"""
    from http://eli.thegreenplace.net/2011/05/26/code-sample-socket-client-based-on-twisted-with-pyqt/
    thanks to Eli Bendersky
    GPL V3
"""
__license__ = """
    Copyright (C) 2008-2011  Avencall <xivo-dev@lists.proformatique.com>

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


from PyQt4.QtCore import *
from PyQt4.QtGui import *


class ConnectIndicator(QWidget):
    def __init__(self, parent=None):
        super(ConnectIndicator, self).__init__(parent)
        self.nframe = 0
        self.setBackgroundRole(QPalette.Base)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.connected = False

    def minimumSizeHint(self):
        return QSize(20, 20)

    def sizeHint(self):
        return QSize(20, 20)
    def next(self):
        self.nframe += 1
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.translate(self.width() / 2, self.height() / 2)

        for diameter in range(0, 20, 9):
            delta = abs((self.nframe % 64) - diameter / 2)
            alpha = 255 - (delta * delta) / 4 - diameter
            if alpha > 0:
                if (self.connected):
                    painter.setPen(QPen(QColor(0, 192, 0, alpha), 3))
                else:    
                    painter.setPen(QPen(QColor(255, 0, 0, alpha), 3))
                painter.drawEllipse(QRectF(
                    -diameter / 2.0,
                    -diameter / 2.0, 
                    diameter, 
                    diameter))