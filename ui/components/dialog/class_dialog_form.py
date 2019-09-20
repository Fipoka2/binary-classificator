# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/design/class_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ClassDialog(object):
    def setupUi(self, ClassDialog):
        ClassDialog.setObjectName("ClassDialog")
        ClassDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ClassDialog.resize(352, 106)
        ClassDialog.setModal(True)
        self.class0Button = QtWidgets.QPushButton(ClassDialog)
        self.class0Button.setGeometry(QtCore.QRect(20, 30, 141, 51))
        self.class0Button.setObjectName("class0Button")
        self.class1Button = QtWidgets.QPushButton(ClassDialog)
        self.class1Button.setGeometry(QtCore.QRect(180, 30, 141, 51))
        self.class1Button.setObjectName("class1Button")

        self.retranslateUi(ClassDialog)
        QtCore.QMetaObject.connectSlotsByName(ClassDialog)

    def retranslateUi(self, ClassDialog):
        _translate = QtCore.QCoreApplication.translate
        ClassDialog.setWindowTitle(_translate("ClassDialog", "Выбор класса"))
        self.class0Button.setText(_translate("ClassDialog", "class 0"))
        self.class1Button.setText(_translate("ClassDialog", "class 1"))

