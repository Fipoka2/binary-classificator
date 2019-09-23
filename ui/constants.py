from enum import Enum

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QColor

WHITE_COLOR = QColor(255, 255, 255)
IMAGE_SIZE = QSize(500, 500)
PREVIEW_SIZE = QSize(180, 180)
MAXPOOL_SIZE = 250

PEN_COLORS = {
    'BLACK': QColor(0, 0, 0),
    'RED': QColor(255, 0, 0),
    'BLUE': QColor(0, 0, 255),
    'GREEN': QColor(0, 255, 0),
    'YELLOW': QColor(255, 255, 0),
    'ORANGE': QColor(250, 165, 10),
    'WHITE': QColor(255, 255, 255),
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


class PenColors(Enum):
    BLACK = QColor(0, 0, 0)
    RED = QColor(255, 0, 0)
    BLUE = QColor(0, 0, 255)
    GREEN = QColor(0, 255, 0)
    YELLOW = QColor(255, 255, 0)
    ORANGE = QColor(250, 165, 10)
    WHITE = QColor(255, 255, 255)


class MessageType(Enum):
    INFO = PenColors.BLACK.value
    WARNING = PenColors.ORANGE.value
    ERROR = PenColors.RED.value
    SUCCESS = PenColors.GREEN.value
