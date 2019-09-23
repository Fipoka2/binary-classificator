import random

from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import (QWidget)

from ui.constants import WHITE_COLOR, IMAGE_SIZE, Spray


class Drawer(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.spray = None
        self.setAttribute(QtCore.Qt.WA_StaticContents)
        self.scribbling = False
        self.penWidth = 7
        self.penColor = QtCore.Qt.black
        self.image = QtGui.QImage(IMAGE_SIZE, QtGui.QImage.Format_RGB32)
        self.image.fill(WHITE_COLOR)
        self.lastPoint = QtCore.QPoint()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(event.rect(), self.image)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.lastPoint = event.pos()
            self.scribbling = True

    def mouseMoveEvent(self, event):
        if (event.buttons() & QtCore.Qt.LeftButton) and self.scribbling:
            self._drawLineTo(event.pos())

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.scribbling:
            self._drawLineTo(event.pos())
            self.scribbling = False

    def _drawLineTo(self, endPoint):
        painter = QtGui.QPainter(self.image)
        painter.setPen(QtGui.QPen(self.penColor,
                                  self.penWidth,
                                  QtCore.Qt.SolidLine,
                                  QtCore.Qt.RoundCap,
                                  QtCore.Qt.RoundJoin))
        if self.spray:
            for n in range(self.spray.spray_particles):
                xo = random.gauss(0, self.spray.spray_diameter)
                yo = random.gauss(0, self.spray.spray_diameter)
                painter.drawPoint(endPoint.x() + xo, endPoint.y() + yo)
        elif self.lastPoint == endPoint:
            painter.drawPoint(endPoint.x(), endPoint.y())
        else:
            painter.drawLine(self.lastPoint, endPoint)

        self.update()
        self.lastPoint = QtCore.QPoint(endPoint)

    def openImage(self, fileName):
        loadedImage = QImage()
        if not loadedImage.load(fileName):
            return False

        self.image = loadedImage.scaled(IMAGE_SIZE)
        self.update()
        return True

    def changePenColor(self, color: QtGui.QColor):
        self.penColor = color

    def changePenSize(self, size: int):
        self.penWidth = size

    def changePenType(self, spray: Spray):
        self.spray = spray

    def clearCanvas(self):
        self.image.fill(WHITE_COLOR)
        self.update()
