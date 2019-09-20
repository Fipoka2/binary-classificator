from PyQt5.QtWidgets import QDialog

from ui.components.dialog.class_dialog_form import Ui_ClassDialog
from ui.constants import DIALOG_SIGNAL_CLASS_0, DIALOG_SIGNAL_CLASS_1


class ClassDialog(QDialog, Ui_ClassDialog):

    def __init__(self, names: tuple, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.changeClassNames(names)

        self.class0Button.clicked.connect(self._selectClass0)
        self.class1Button.clicked.connect(self._selectClass1)

    def _selectClass0(self):
        self.done(DIALOG_SIGNAL_CLASS_0)

    def _selectClass1(self):
        self.done(DIALOG_SIGNAL_CLASS_1)

    def changeClassNames(self, names: tuple):
        a, b = names
        self.class0Button.setText(a)
        self.class1Button.setText(b)
