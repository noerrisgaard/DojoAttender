# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'transfer_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DataTransfer(object):
    def setupUi(self, DataTransfer):
        DataTransfer.setObjectName("DataTransfer")
        DataTransfer.setWindowModality(QtCore.Qt.ApplicationModal)
        DataTransfer.resize(342, 80)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DataTransfer.sizePolicy().hasHeightForWidth())
        DataTransfer.setSizePolicy(sizePolicy)
        DataTransfer.setMinimumSize(QtCore.QSize(342, 80))
        DataTransfer.setMaximumSize(QtCore.QSize(342, 80))
        DataTransfer.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0, stop:0 rgba(37, 117, 91, 255), stop:1 rgba(255, 255, 255, 255));")
        DataTransfer.setSizeGripEnabled(False)
        DataTransfer.setModal(True)
        self.label = QtWidgets.QLabel(DataTransfer)
        self.label.setGeometry(QtCore.QRect(0, -30, 341, 111))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.CancelBtn = QtWidgets.QPushButton(DataTransfer)
        self.CancelBtn.setGeometry(QtCore.QRect(90, 50, 161, 23))
        self.CancelBtn.setObjectName("CancelBtn")

        self.retranslateUi(DataTransfer)
        QtCore.QMetaObject.connectSlotsByName(DataTransfer)

    def retranslateUi(self, DataTransfer):
        _translate = QtCore.QCoreApplication.translate
        DataTransfer.setWindowTitle(_translate("DataTransfer", "Data Transfer"))
        self.label.setText(_translate("DataTransfer", "Please insert USB stick/flash drive"))
        self.CancelBtn.setText(_translate("DataTransfer", "Cancel"))

