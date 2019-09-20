from PyQt5 import QtGui
from PyQt5.QtCore import QSize

WHITE_COLOR = QtGui.QColor(255, 255, 255)
IMAGE_SIZE = QSize(500, 500)
PREVIEW_SIZE = QSize(180, 180)

PEN_COLORS = {
    'BLACK': QtGui.QColor(0, 0, 0),
    'RED': QtGui.QColor(255, 0, 0),
    'BLUE': QtGui.QColor(0, 0, 255),
    'GREEN': QtGui.QColor(0, 255, 0),
    'YELLOW': QtGui.QColor(255, 255, 0),
    'ORANGE': QtGui.QColor(250, 165, 10),
    'WHITE': QtGui.QColor(255, 255, 255),
}


class Spray:
    def __init__(self, particles=100, diameter=10):
        self.spray_particles = particles
        self.spray_diameter = diameter


PEN_TYPES = {
    'NORMAL': None,
    'SPRAY_SMALL': Spray(5, 2),
    'SPRAY_MEDIUM': Spray(50, 5),
    'SPRAY_LARGE': Spray()
}

DIALOG_SIGNAL_CLASS_0 = 10
DIALOG_SIGNAL_CLASS_1 = 11
