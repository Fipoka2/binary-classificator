from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QImage, QPainterPath
from PyQt5.QtWidgets import QFrame

from ui.constants import WHITE_COLOR, PREVIEW_SIZE


class PreviewBox(QFrame):
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)
        self.setAttribute(QtCore.Qt.WA_StaticContents)
        self.image = QtGui.QImage(PREVIEW_SIZE, QtGui.QImage.Format_RGB32)
        self.image.fill(WHITE_COLOR)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(event.rect(), self.image)

        rectPath = QPainterPath()
        rectPath.addRect(QRectF(0, 0, self.width() - 1, self.height() - 1))
        painter.drawPath(rectPath)

    def setImage(self, selectedImage: QImage):
        self.image = selectedImage.scaled(PREVIEW_SIZE)
        self.update()
